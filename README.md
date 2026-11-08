# Trading Performance Cockpit

Cockpit d'aide à la décision pour scalping et day trading, priorité Gold / SMC.

## Configuration
- Autorité : ASSIST — le cockpit vérifie et guide, la décision d'entrée reste humaine.
- Signaux : BOTH — pré-alerte de sweep puis confirmation par displacement, MSS et FVG.
- Risque de référence : plafond interne 0,50 % par trade (pas une règle officielle FTMO/Vantage).
- Profils : FTMO et Vantage.
- Données : TradingView intégré + pont MT5 local en lecture seule, sans ordre automatique.

## Connexion MT5 en direct
1. Sur le PC Windows qui exécute MT5, télécharge `install_mt5_bridge.bat` depuis ce dépôt.
2. Installe Python 3.11 ou 3.12 64 bits si nécessaire, puis double-clique l'installateur.
3. Ouvre MT5, connecte-toi au compte FTMO ou Vantage, puis lance `start_mt5_bridge.bat` dans le dossier local.
4. Copie la clé locale affichée dans la fenêtre du pont.
5. Ouvre le cockpit, dans **MT5 Live Feed**, colle la clé et sélectionne le même profil que le terminal ouvert.
6. Vérifie le serveur, le compte masqué et le symbole exact du Gold dans Market Watch. Modifie les correspondances de symboles si le broker utilise un suffixe.

Le pont réutilise le terminal MT5 déjà authentifié ; aucun mot de passe de compte n'est stocké ni transmis par le cockpit. Pour deux installations distinctes, renseigne les chemins `terminal64.exe` et `server_hint` dans `bridge_config.local.json`. Un seul terminal est connecté au pont à la fois.

## Données MT5
Le pont lit les ticks Bid/Ask, les bougies M1/M5/M15/M30/H1/H4/D1/W1, les spécifications du symbole, l'equity, la marge, les positions et le P&L journalier calculé depuis minuit UTC. Le navigateur actualise les ticks toutes les 1,5 seconde environ et les historiques multi-actifs toutes les 8 secondes. C'est du polling local, pas un flux WebSocket tick-by-tick.

Les noms de symboles varient selon les serveurs. Le Gold est requis ; DXY, Silver, EURUSD, GBPUSD et USDJPY sont facultatifs pour le radar inter-marchés. Si un actif n'existe pas dans le Market Watch du compte connecté, le moteur affiche une erreur pour cet actif sans inventer de données.

## Sécurité et limites
- `mt5_readonly_bridge.py` écoute exclusivement sur `127.0.0.1:8765`.
- Le pont ne contient aucune fonction d'envoi, modification ou fermeture d'ordre. L'exécution se fait manuellement dans MT5.
- La clé API est créée dans le fichier local `bridge_config.local.json`; ne la publie jamais et ne la partage pas.
- Les données de compte sont lues depuis MT5 local et affichées dans le navigateur. Pas de connexion au compte TradingView ni de collecte de mot de passe.
- Le P&L du pont est basé sur minuit UTC ; les règles et dates de calcul prop firm peuvent différer et inclure les pertes flottantes.
- Les cotations MT5 sont propres au terminal/serveur connecté ; TradingView peut afficher un prix différent.
- Un tick périmé, un historique manquant ou un risque de position non calculable doit être traité comme une condition de prudence. Le bouton STOP du cockpit n'envoie pas d'ordre de fermeture.

## Analyse
Le Market Intelligence utilise les bougies MT5 importées automatiquement lorsque le pont est connecté. Les CSV TradingView restent disponibles comme solution de secours. Les indicateurs de structure, ATR, corrélation et SMT sont heuristiques ; un SMT ou une pré-alerte ne constitue pas une entrée. Les résultats doivent être validés sur historique hors échantillon, avec frais et slippage.

Le cockpit est un outil d'organisation et de contrôle, pas un conseil financier. Aucun signal, automatisme ni paramètre ne garantit une session rentable.

## Publication
GitHub Pages : https://rocalle58-create.github.io/session-desk/

## Trade Command Center — mode manuel
L'onglet **06 · Trade Command Center** regroupe :
- **Liquidity Radar** : PDH/PDL, PWH/PWL, PMH/PML et plages Asia/London/New York calculées sur les bougies MT5 reçues (heure de Paris).
- **Smart Money Scanner** : sweep, rupture de pivots, displacement, FVG, OB candidat et premium/discount sur bougies clôturées. Les lectures restent heuristiques et doivent être contrôlées visuellement.
- **Session Control** : fenêtres horaires configurables en heure de Paris.
- **Risk Guardian** : tick, spread, marge, positions sans SL, risque ouvert et P&L quotidien réalisé + flottant du pont (UTC). Les seuils sont réglables.
- **News Shock Radar** : événements à fort impact saisis manuellement avec fenêtre de prudence avant/après. Le calendrier TradingView embarqué n'est pas lu automatiquement par le site.
- **Performance Lab** : stats des positions clôturées via l'endpoint local `/api/history`, commissions/swaps/frais inclus. Les positions toujours ouvertes sont exclues.
- **Alert Engine** : alertes en page et notifications navigateur optionnelles. Le navigateur et le pont doivent rester actifs.

### Mise à jour du connecteur
Relance `install_mt5_bridge.bat` pour récupérer le nouveau pont dans `%USERPROFILE%\TradingPerformanceCockpit\MT5Bridge`. Le script préserve `bridge_config.local.json` et donc la clé locale. Puis relance `start_mt5_bridge.bat`. L'endpoint d'historique est strictement en lecture seule. Aucune fonction d'envoi, modification ou fermeture d'ordre n'est présente.
