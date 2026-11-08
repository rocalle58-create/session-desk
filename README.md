# Trading Performance Cockpit

Cockpit web de trading pour le scalping et le day trading, priorité Gold, profils FTMO et Vantage.

## Modules
- Briefing pré-session, checklist de départ, statut de session et verrouillage.
- Market Radar multi-actifs, biais HTF/intraday, PDH/PDL, PWH/PWL, extrêmes de session et PD Arrays.
- Graphiques et ruban de cotations TradingView.
- Flux MT5 local distinct : Bid/Ask, spread, spécifications du symbole, equity, marge, positions ouvertes, P&L réalisé journalier et risque ouvert.
- Détecteur expérimental du Setup A sur bougies MT5 clôturées (sweep, displacement, MSS, FVG).
- Ticket indicatif, calcul du volume avec tick size / tick value fournis par le terminal MT5.
- Risk Guardian, interlocks, verrou de session, journal, métriques de performance et export JSON.
- Actualisation périodique des positions, du P&L, des cotations et du moteur de détection.

## Connexion MT5 sur Windows
1. Télécharge et extrais le paquet [MT5 Bridge Windows](https://github.com/rocalle58-create/session-desk/raw/refs/heads/main/mt5-bridge-windows.zip) sur le PC où MT5 est installé.
2. Installe Python 3 64 bits compatible avec le package MetaTrader5.
3. Ouvre MT5 FTMO ou Vantage et connecte-toi au compte voulu. Vérifie le nom exact du symbole dans Market Watch.
4. Copie `bridge_config.example.json` en `bridge_config.local.json`. Modifie les chemins des deux terminaux dans ce fichier ; les chemins d'exemple sont à adapter.
5. Laisse `allow_live_orders` à `false`, puis lance `start_bridge.bat`. Le premier démarrage installe les dépendances, crée la clé locale et démarre le service sur `127.0.0.1:8765`.
6. Clique sur « Connecter MT5 » dans le cockpit, garde l'adresse `http://127.0.0.1:8765`, puis colle la clé affichée dans la fenêtre du pont.
7. Choisis FTMO ou Vantage dans le cockpit. Un seul terminal alimente le cockpit à la fois ; changer de profil ferme la connexion MT5 active et connecte l'autre terminal.

Le navigateur peut demander une autorisation d'accès au réseau local. Ne change jamais le pont pour l'exposer sur Internet.

## Automatisation et sécurité
- Le mode automatique surveille, actualise, calcule, détecte un candidat de setup et applique les verrous. Il ne garantit aucun résultat.
- Le détecteur ne couvre actuellement que le Setup A. Les seuils sont expérimentaux ; backtest, test hors échantillon et forward test sont nécessaires.
- Les ordres live sont désactivés par défaut dans la configuration locale. Un signal ne déclenche jamais un ordre automatiquement : la session doit être démarrée, les contrôles doivent être valides, le setup vérifié, une confirmation cochée et l'ordre confirmé séparément.
- Le pont contrôle le compte, la distance d'entrée au prix actuel, le sens du SL/TP, le spread, le volume, le risque au stop, le risque ouvert, la perte réalisée journalière et la marge. Les contrôles sont des garde-fous supplémentaires, pas une garantie.
- Le P&L journalier utilisé par le pont est calculé depuis minuit UTC. La journée du serveur peut différer et les limites prop firm peuvent intégrer les pertes flottantes : ce chiffre est indicatif et ne remplace pas les règles officielles.
- Les commissions et le slippage peuvent augmenter la perte réelle. Vérifie les spécifications de chaque symbole et commence en démo.
- Les cotations TradingView peuvent différer du Bid/Ask du terminal ; le prix MT5 du compte sélectionné fait foi pour le ticket.
- « STOP SESSION » bloque les nouvelles autorisations du cockpit mais ne ferme pas les positions ouvertes et ne remplace pas les stops serveur.

## Données locales
Configuration et journal sont enregistrés sur l'appareil/navigateur. Exporte régulièrement le journal JSON. Le fichier `bridge_config.local.json` contient la clé locale et les chemins privés : ne le publie jamais sur GitHub et ne partage pas tes identifiants MT5.

Outil d'organisation et de contrôle, pas un conseil financier. Aucun signal, réglage ou garde-fou ne garantit une session rentable.
