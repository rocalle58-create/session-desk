"""Local read-only MT5 data bridge for Trading Performance Cockpit.
Binds only to loopback; intentionally has no order placement/modification route.
"""
from __future__ import annotations
import json, secrets, threading, time, csv, io, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
CFG = ROOT / "bridge_config.local.json"
EXAMPLE = ROOT / "bridge_config.example.json"
HOST, PORT, VERSION = "127.0.0.1", 8765, "2.2-readonly-command-center"
ORIGINS = {"https://rocalle58-create.github.io", "http://127.0.0.1:8000", "http://localhost:8000", "http://127.0.0.1:5500", "http://localhost:5500"}
LOCK = threading.RLock()
mt5 = None
active_profile = None

DEFAULT = {"api_key": "", "profile": "FTMO", "terminals": {
    "FTMO": {"path": "", "server_hint": ""}, "Vantage": {"path": "", "server_hint": ""}}}

def config_load():
    if CFG.exists(): data = json.loads(CFG.read_text(encoding="utf-8"))
    elif EXAMPLE.exists(): data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    else: data = json.loads(json.dumps(DEFAULT))
    data.setdefault("terminals", {})
    for p in ("FTMO", "Vantage"): data["terminals"].setdefault(p, {"path": "", "server_hint": ""})
    if not data.get("api_key"): data["api_key"] = secrets.token_urlsafe(32)
    CFG.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data

CONFIG = config_load()


# Public macro observations downloaded from FRED graph CSV exports.
# Values are publication-frequency data, not real-time market ticks.
MACRO_SERIES = {
    "DGS10": {"label": "US 10Y nominal yield", "kind": "rate", "threshold": 0.05, "lookback": 5},
    "DFII10": {"label": "US 10Y real yield", "kind": "rate", "threshold": 0.05, "lookback": 5},
    "DFF": {"label": "Effective federal funds rate", "kind": "rate", "threshold": 0.025, "lookback": 20},
    "CPIAUCSL": {"label": "CPI, all items", "kind": "inflation"},
    "PCEPILFE": {"label": "PCE price index excluding food and energy", "kind": "inflation"},
}
MACRO_CACHE = {"at": 0.0, "data": None}
MACRO_CACHE_LOCK = threading.Lock()

def _fetch_fred_series(series_id):
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=" + series_id
    req = urllib.request.Request(url, headers={"User-Agent": "TradingPerformanceCockpit/2.1"})
    with urllib.request.urlopen(req, timeout=12) as response:
        raw = response.read().decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(raw)))
    points = []
    for row in rows:
        date = row.get("observation_date") or row.get("DATE") or row.get("date")
        value = row.get(series_id)
        if not date or value in (None, "", "."):
            continue
        try:
            points.append({"date": date, "value": float(value)})
        except (TypeError, ValueError):
            continue
    if not points:
        raise RuntimeError("No valid observations returned for " + series_id)
    meta = MACRO_SERIES[series_id]
    latest = points[-1]
    result = {"id": series_id, "label": meta["label"], "latest": latest["value"],
              "latest_date": latest["date"], "trend": None, "delta": None,
              "unit": "%" if meta["kind"] == "rate" else "index"}
    if meta["kind"] == "rate":
        back = meta["lookback"]
        if len(points) > back:
            delta = latest["value"] - points[-1-back]["value"]
            result["delta"] = round(delta, 4)
            result["trend"] = "up" if delta >= meta["threshold"] else "down" if delta <= -meta["threshold"] else "flat"
    else:
        if len(points) >= 14:
            yoy = (latest["value"] / points[-13]["value"] - 1.0) * 100.0
            prev_yoy = (points[-2]["value"] / points[-14]["value"] - 1.0) * 100.0
            result["yoy_pct"] = round(yoy, 3)
            result["yoy_change"] = round(yoy - prev_yoy, 3)
    return result

def fred_macro_data():
    now = time.time()
    with MACRO_CACHE_LOCK:
        if MACRO_CACHE["data"] is not None and now - MACRO_CACHE["at"] < 900:
            cached = dict(MACRO_CACHE["data"])
            cached["cached"] = True
            return cached
        results, errors = {}, {}
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = {pool.submit(_fetch_fred_series, sid): sid for sid in MACRO_SERIES}
            for future in as_completed(futures):
                sid = futures[future]
                try:
                    results[sid] = future.result()
                except Exception as exc:
                    errors[sid] = str(exc)
        if not results and MACRO_CACHE["data"] is not None:
            stale = dict(MACRO_CACHE["data"])
            stale["cached"] = True
            stale["stale"] = True
            stale["errors"] = errors
            return stale
        if not results:
            raise RuntimeError("FRED data could not be reached: " + "; ".join(errors.values()))
        payload = {"source": "FRED graph CSV", "updated_at": datetime.now(timezone.utc).isoformat(),
                   "series": results, "series_count": len(results), "errors": errors,
                   "cached": False, "stale": False}
        MACRO_CACHE["at"], MACRO_CACHE["data"] = now, payload
        return payload

def api():
    global mt5
    if mt5 is None:
        try: import MetaTrader5 as lib
        except ImportError as e: raise RuntimeError("Package MetaTrader5 absent. Lance start_mt5_bridge.bat pour l'installer ; Python 3.11/3.12 64 bits est requis.") from e
        mt5 = lib
    return mt5

def connected():
    lib = api(); terminal = lib.terminal_info(); account = lib.account_info()
    if terminal is None or account is None: raise RuntimeError(f"MT5 non connecté. Ouvre le terminal et connecte-toi au compte. Détail : {lib.last_error()}")
    return lib, terminal, account

def account_json(account, terminal, profile=None):
    login = str(getattr(account, "login", ""))
    return {"profile": profile or active_profile, "login_masked": ("••••" + login[-4:]) if login else "Masqué",
        "server": str(account.server), "company": str(getattr(terminal, "company", "")),
        "terminal_name": str(getattr(terminal, "name", "MetaTrader 5")), "currency": str(account.currency),
        "balance": float(account.balance), "equity": float(account.equity), "margin": float(account.margin),
        "margin_free": float(account.margin_free), "leverage": int(getattr(account, "leverage", 0)),
        "trade_allowed": bool(getattr(terminal, "trade_allowed", False) and getattr(account, "trade_allowed", False))}

def connect(profile):
    global active_profile
    if profile not in ("FTMO", "Vantage"): raise ValueError("Choisis FTMO ou Vantage.")
    lib = api(); opt = CONFIG["terminals"][profile]; path = str(opt.get("path", "")).strip(); hint = str(opt.get("server_hint", "")).strip()
    with LOCK:
        lib.shutdown()
        if not (lib.initialize(path) if path else lib.initialize()): raise RuntimeError(f"Initialisation MT5 impossible : {lib.last_error()}. Vérifie que le terminal est installé et connecté.")
        terminal, account = lib.terminal_info(), lib.account_info()
        if terminal is None or account is None: lib.shutdown(); raise RuntimeError("Le terminal ne présente aucun compte connecté.")
        if hint and hint.lower() not in str(account.server).lower():
            actual = str(account.server); lib.shutdown(); raise RuntimeError(f"Mauvais serveur : {actual}. Le profil {profile} attend un serveur contenant {hint}.")
        active_profile = profile; CONFIG["profile"] = profile; CFG.write_text(json.dumps(CONFIG, indent=2, ensure_ascii=False), encoding="utf-8")
        return account_json(account, terminal, profile)

def quote(symbol):
    lib = api(); symbol = symbol.strip()
    if not symbol: raise ValueError("Symbole MT5 vide.")
    info = lib.symbol_info(symbol)
    if info is None: raise ValueError(f"Symbole {symbol} introuvable. Vérifie le nom exact dans Market Watch (suffixes broker possibles).")
    if not info.visible and not lib.symbol_select(symbol, True): raise RuntimeError(f"Impossible d'afficher {symbol} dans Market Watch.")
    tick = lib.symbol_info_tick(symbol)
    if tick is None: raise RuntimeError(f"Aucune cotation sur {symbol}.")
    point = float(info.point or 0); bid, ask = float(tick.bid), float(tick.ask)
    tms = int(getattr(tick, "time_msc", 0) or int(tick.time)*1000); age = max(0, time.time()-tms/1000)
    meta = {"digits": int(info.digits), "point": point, "volume_min": float(info.volume_min), "volume_max": float(info.volume_max),
        "volume_step": float(info.volume_step), "trade_tick_size": float(getattr(info,"trade_tick_size",0) or 0),
        "trade_tick_value": float(getattr(info,"trade_tick_value",0) or 0), "trade_tick_value_loss": float(getattr(info,"trade_tick_value_loss",0) or 0),
        "trade_contract_size": float(getattr(info,"trade_contract_size",0) or 0), "trade_stops_level": int(getattr(info,"trade_stops_level",0) or 0),
        "spread_points": ((ask-bid)/point if point else None)}
    return {"symbol":symbol,"bid":bid,"ask":ask,"last":float(getattr(tick,"last",0) or 0),"time":int(tick.time),"time_msc":tms,"age_seconds":round(age,2),"stale":age>15,"meta":meta}

TF = {"M1":"TIMEFRAME_M1","M5":"TIMEFRAME_M5","M15":"TIMEFRAME_M15","M30":"TIMEFRAME_M30","H1":"TIMEFRAME_H1","H4":"TIMEFRAME_H4","D1":"TIMEFRAME_D1","W1":"TIMEFRAME_W1"}
def bars(symbol, tf, count):
    lib=api(); tf=tf.upper()
    if tf not in TF: raise ValueError("Timeframe non supporté : "+tf)
    rates=lib.copy_rates_from_pos(symbol,getattr(lib,TF[tf]),0,count)
    if rates is None: raise RuntimeError(f"Historique {symbol} {tf} indisponible : {lib.last_error()}")
    return [{"time":int(r["time"]),"open":float(r["open"]),"high":float(r["high"]),"low":float(r["low"]),"close":float(r["close"]),"tick_volume":int(r["tick_volume"])} for r in sorted(rates,key=lambda x:int(x["time"]))]

def positions_data():
    lib=api(); rows=lib.positions_get()
    if rows is None: return [], None
    items=[]; total=0.0; known=True
    for p in rows:
        buy=int(p.type)==int(lib.POSITION_TYPE_BUY); side="BUY" if buy else "SELL"; risk=None
        if p.sl:
            kind=lib.ORDER_TYPE_BUY if buy else lib.ORDER_TYPE_SELL
            loss=lib.order_calc_profit(kind,p.symbol,float(p.volume),float(p.price_open),float(p.sl))
            if loss is None: known=False
            else: risk=max(0.0,-float(loss)); total+=risk
        else: known=False
        items.append({"ticket":int(p.ticket),"symbol":p.symbol,"side":side,"volume":float(p.volume),"open":float(p.price_open),"sl":float(p.sl),"tp":float(p.tp),"profit":float(p.profit),"swap":float(p.swap),"risk_to_sl":risk})
    return items, total if known else None

def history_deals(days=90, symbol_filter=""):
    """Read-only deal history for performance analytics; never accesses order placement."""
    lib=api()
    now=datetime.now(timezone.utc)
    start=now-timedelta(days=max(1,min(int(days),365)))
    deals=lib.history_deals_get(start,now)
    if deals is None:
        raise RuntimeError(f"Historique des deals indisponible : {lib.last_error()}")
    rows=[]
    for d in deals:
        symbol=str(getattr(d,"symbol","") or "")
        if symbol_filter and symbol_filter.upper() not in symbol.upper():
            continue
        rows.append({
            "ticket": int(getattr(d,"ticket",0) or 0),
            "position_id": int(getattr(d,"position_id",0) or 0),
            "time": int(getattr(d,"time",0) or 0),
            "time_msc": int(getattr(d,"time_msc",0) or 0),
            "symbol": symbol,
            "type": int(getattr(d,"type",-1)),
            "entry": int(getattr(d,"entry",-1)),
            "volume": float(getattr(d,"volume",0) or 0),
            "price": float(getattr(d,"price",0) or 0),
            "profit": float(getattr(d,"profit",0) or 0),
            "commission": float(getattr(d,"commission",0) or 0),
            "swap": float(getattr(d,"swap",0) or 0),
            "fee": float(getattr(d,"fee",0) or 0),
            "comment": str(getattr(d,"comment","") or "")
        })
    open_rows=lib.positions_get() or []
    open_ids=[int(getattr(p,"identifier",getattr(p,"ticket",0)) or 0) for p in open_rows]
    return {"days":int(days),"from":start.isoformat(),"to":now.isoformat(),
            "count":len(rows),"deals":rows,"open_position_ids":open_ids,"read_only":True}

def daily_pnl():
    lib=api(); now=datetime.now(timezone.utc); start=now.replace(hour=0,minute=0,second=0,microsecond=0)
    deals=lib.history_deals_get(start,now)
    if deals is None: return None
    return sum(float(getattr(d,"profit",0))+float(getattr(d,"commission",0))+float(getattr(d,"swap",0))+float(getattr(d,"fee",0)) for d in deals)

class Handler(BaseHTTPRequestHandler):
    server_version="TPC-MT5-Readonly/"+VERSION
    def log_message(self, fmt, *args): print("["+datetime.now().strftime("%H:%M:%S")+"] "+(fmt % args))
    def cors(self):
        origin=self.headers.get("Origin","")
        if origin in ORIGINS: self.send_header("Access-Control-Allow-Origin",origin); self.send_header("Vary","Origin")
        self.send_header("Access-Control-Allow-Methods","GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type, X-API-Key")
        if self.headers.get("Access-Control-Request-Private-Network","").lower()=="true": self.send_header("Access-Control-Allow-Private-Network","true")
    def out(self,status,data):
        body=json.dumps(data,ensure_ascii=False,separators=(",",":")).encode()
        self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Content-Length",str(len(body))); self.send_header("Cache-Control","no-store"); self.cors(); self.end_headers(); self.wfile.write(body)
    def do_OPTIONS(self): self.send_response(204); self.send_header("Content-Length","0"); self.cors(); self.end_headers()
    def auth(self):
        origin=self.headers.get("Origin","")
        if origin and origin not in ORIGINS: self.out(403,{"error":"Origine non autorisée."}); return False
        if not secrets.compare_digest(self.headers.get("X-API-Key",""),str(CONFIG["api_key"])): self.out(401,{"error":"Clé locale absente ou incorrecte."}); return False
        return True
    def body(self):
        n=int(self.headers.get("Content-Length","0") or 0)
        if n>4096: raise ValueError("Requête trop volumineuse.")
        x=json.loads(self.rfile.read(n).decode() if n else "{}")
        if not isinstance(x,dict): raise ValueError("JSON invalide.")
        return x
    def do_GET(self):
        p=urlparse(self.path); q=parse_qs(p.query)
        if p.path=="/health": self.out(200,{"ok":True,"service":"TPC MT5 read-only","version":VERSION}); return
        if not self.auth(): return
        try:
            if p.path=="/api/macro": self.out(200,fred_macro_data()); return
            with LOCK:
                if p.path=="/api/history":
                    days=min(365,max(1,int((q.get("days") or ["90"])[0])))
                    symbol_filter=(q.get("symbol") or [""])[0].strip()
                    self.out(200,history_deals(days,symbol_filter)); return
                if p.path=="/api/status":
                    lib,t,a=connected(); pos,risk=positions_data(); pnl=daily_pnl(); floating=sum(x["profit"]+x["swap"] for x in pos)
                    self.out(200,{"connected":True,"profile":active_profile,"account":account_json(a,t),"positions":pos,"positions_count":len(pos),"open_risk_cash":risk,"daily_realized_pnl_utc":pnl,"daily_pnl_utc_with_floating":pnl+floating if pnl is not None else None,"read_only":True}); return
                if p.path=="/api/market-pack":
                    lib,t,a=connected(); requested=list(dict.fromkeys(x.strip() for x in (q.get("symbols") or [""])[0].split(",") if x.strip()))[:8]
                    tfs=list(dict.fromkeys(x.strip().upper() for x in (q.get("timeframes") or ["M1,M5,M15,M30,H1,H4,D1,W1"])[0].split(",") if x.strip().upper() in TF))[:8]
                    count=min(350,max(55,int((q.get("count") or ["180"])[0]))); markets={}; errors={}
                    for sym in requested:
                        try:
                            qq=quote(sym); series={}
                            for tf in tfs:
                                try: series[tf]=bars(sym,tf,count)
                                except Exception as e: errors[sym+"_"+tf]=str(e)
                            markets[sym]={"quote":qq,"rates":series}
                        except Exception as e: errors[sym]=str(e)
                    pos,risk=positions_data(); pnl=daily_pnl(); floating=sum(x["profit"]+x["swap"] for x in pos)
                    self.out(200,{"connected":True,"profile":active_profile,"account":account_json(a,t),"markets":markets,"errors":errors,"positions":pos,"positions_count":len(pos),"open_risk_cash":risk,"daily_realized_pnl_utc":pnl,"daily_pnl_utc_with_floating":pnl+floating if pnl is not None else None,"server_time":int(time.time()),"read_only":True}); return
                if p.path=="/api/symbols":
                    lib,_,_=connected(); needle=(q.get("q") or [""])[0].lower(); found=[]
                    for x in lib.symbols_get() or []:
                        if needle in x.name.lower(): found.append({"name":x.name,"description":str(getattr(x,"description",""))})
                        if len(found)>=100: break
                    self.out(200,{"symbols":found}); return
                if p.path=="/api/quote": self.out(200,quote((q.get("symbol") or [""])[0])); return
                self.out(404,{"error":"Route inconnue."})
        except Exception as e: self.out(400,{"error":str(e)})
    def do_POST(self):
        if not self.auth(): return
        try:
            body=self.body()
            with LOCK:
                if urlparse(self.path).path=="/api/connect": self.out(200,{"connected":True,"account":connect(str(body.get("profile","FTMO"))),"read_only":True}); return
                if urlparse(self.path).path=="/api/disconnect": api().shutdown(); self.out(200,{"connected":False}); return
                self.out(404,{"error":"Route inconnue. Le pont fonctionne en lecture seule."})
        except Exception as e: self.out(400,{"error":str(e)})

def main():
    print("\nTPC MT5 Bridge — lecture seule · http://127.0.0.1:8765")
    print("Aucune fonction d'envoi d'ordre n'est présente dans ce pont.")
    print("Clé API locale à coller dans le cockpit (ne pas partager) :\n"+CONFIG["api_key"])
    print("Laisse cette fenêtre ouverte pendant la session. Ctrl+C pour arrêter.\n")
    server=ThreadingHTTPServer((HOST,PORT),Handler)
    try: server.serve_forever(poll_interval=.5)
    except KeyboardInterrupt: print("Arrêt du pont.")
    finally:
        server.server_close()
        if mt5 is not None:
            try: mt5.shutdown()
            except Exception: pass

if __name__=="__main__": main()
