# Trading Performance Cockpit

Cockpit web personnel de trading mixte (scalping + day trading), priorité Gold, profils FTMO et Vantage.

## Modules du cockpit
- Dashboard pit-wall : heure de Paris, état du pont, état du garde-fou et feux de départ.
- Préparation de session et checklist bloquante.
- Market Radar : Gold, DXY, EURUSD, GBPUSD, USDJPY, Silver ; biais HTF/intraday, liquidités PDH/PDL, PWH/PWL et plages de session.
- Graphiques et ruban de cotations TradingView.
- Flux MT5 local : Bid/Ask, spread, spécifications du symbole, equity, marge, positions, P&L réalisé journalier et risque ouvert.
- Détecteur expérimental de candidat Setup A sur bougies clôturées (sweep, displacement, MSS, FVG).
- Ticket d'exécution avec calcul de volume fondé sur tick size/tick value du terminal MT5.
- Risk Guardian, verrous de sécurité, journal, statistiques de performance et export JSON.
- Rafraîchissement périodique et surveillance automatique de la session.

## Installer le pont MT5 Windows
1. Télécharge le fichier `install_mt5_bridge.ps1` depuis ce dépôt (bouton de connexion MT5 dans le cockpit).
2. Sur le PC Windows qui exécute MT5, ouvre PowerShell et lance le script téléchargé. Il reconstitue le ZIP du pont et ouvre son dossier d'installation.
3. Installe Python 3 64 bits compatible avec le package `MetaTrader5`.
4. Ouvre MT5 FTMO ou Vantage et connecte-toi au compte voulu. Vérifie le nom exact du symbole Gold dans Market Watch.
5. Copie `bridge_config.example.json` en `bridge_config.local.json`. Modifie les chemins `terminal64.exe` FTMO et Vantage selon ton installation ; ne publie jamais ce fichier.
6. Laisse `allow_live_orders` à `false` et lance `start_bridge.bat`. Le premier démarrage installe les dépendances, génère une clé API locale et démarre le service sur `127.0.0.1:8765`.
7. Dans le cockpit, clique « Connecter MT5 », garde `http://127.0.0.1:8765`, colle la clé locale et sélectionne FTMO ou Vantage.
8. Un seul terminal alimente le cockpit à la fois. Le changement de profil ferme la connexion active avant d'initialiser l'autre terminal.

Si Windows bloque le script téléchargé, ouvre PowerShell dans son dossier et lance :
```powershell
Set-ExecutionPolicy -Scope Process Bypass -Force
.\install_mt5_bridge.ps1
```

Le navigateur peut demander l'autorisation d'accéder au réseau local. Le pont doit rester lié à `127.0.0.1` ; ne l'expose jamais sur Internet.

## Automatisation et sécurité
- Le mode auto actualise les données, analyse périodiquement les bougies clôturées, calcule les lots et applique les contrôles. Il ne garantit aucun résultat.
- Le détecteur actuel ne couvre que le Setup A expérimental. Les signaux doivent être vérifiés sur le graphique, puis backtestés hors échantillon, avec spread, commissions et slippage.
- Les ordres live sont désactivés par défaut (`allow_live_orders: false`). Le cockpit ne déclenche pas d'ordre à partir d'un signal seul : session démarrée, connexion saine, contrôles valides, setup confirmé, case de confirmation cochée et confirmation explicite de l'ordre sont requis.
- Le pont contrôle le compte sélectionné, l'écart prix/ticket, le sens du SL/TP, le spread, le volume, le risque au stop, l'exposition ouverte, la perte réalisée journalière et la marge. Les contrôles sont des garde-fous supplémentaires, pas une garantie.
- Le P&L journalier du pont est calculé depuis minuit UTC à partir des deals MT5 ; la journée serveur et les règles prop firm peuvent différer et intégrer des pertes flottantes. Il reste indicatif.
- Commissions, swaps, slippage et gaps peuvent augmenter la perte réelle. Commence en démo et vérifie les spécifications du symbole.
- Les cours TradingView peuvent différer du Bid/Ask de ton compte MT5. Pour le ticket, les prix du terminal sélectionné font foi.
- STOP SESSION bloque les nouvelles autorisations du cockpit ; il ne ferme pas les positions ouvertes et ne remplace pas les stops serveur.
- Le mode auto n'est pas une promesse d'exécution entièrement autonome : les ordres réels requièrent une validation humaine.

## Données et confidentialité
- La configuration du cockpit et les journaux sont stockés localement dans le navigateur.
- La clé API et les chemins des terminaux sont stockés dans la configuration locale ou le navigateur, jamais dans les fichiers publiés.
- Exporte régulièrement le journal JSON pour conserver une sauvegarde.

## Déploiement
GitHub Pages est publié depuis `rocalle58-create/session-desk`. Le workflow `.github/workflows/pages.yml` publie à chaque mise à jour de `main`. L'application compressée est découpée en douze fragments `app-v2-part-*.txt`, réunis à l'ouverture par `index.html`.

Outil d'organisation et de contrôle, pas un conseil financier. Aucune checklist, détection ou règle de risque ne garantit une session rentable.
