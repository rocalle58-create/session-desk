# Trading Performance Cockpit

Cockpit web de trading pour le scalping et le day trading, priorité Gold, profils FTMO et Vantage.

## Modules web
- Cockpit de session, checklist pré-départ et feux vert/orange/rouge.
- Radar multi-actifs, contexte macro, niveaux de liquidité et widgets TradingView.
- Détecteur expérimental de setups sur bougies clôturées MT5.
- Préparation d'ordre, calcul du volume selon les spécifications du symbole.
- Risk Guardian, exposition ouverte, limite journalière, verrous et journal local.
- Pont Windows local MetaTrader 5 : cotations Bid/Ask, bougies closes, positions et prévalidation.

## Installation du pont MT5 (Windows)
1. Télécharge `mt5-bridge-windows.zip` depuis ce dépôt et extrais-le dans un dossier local.
2. Installe MT5 pour FTMO et/ou Vantage et connecte-toi au terminal voulu.
3. Installe Python 64 bits sur le même PC.
4. Copie `bridge_config.example.json` en `bridge_config.local.json`.
5. Remplace les chemins d'exemple par les chemins réels vers `terminal64.exe` de FTMO et Vantage.
6. Garde `allow_live_orders: false` pendant les essais.
7. Lance `start_bridge.bat`. Au premier lancement, les dépendances sont installées et une clé locale est générée.
8. Copie cette clé dans le cockpit, ouvre Connecter MT5 et sélectionne le profil du terminal actuellement ouvert.

Le pont écoute uniquement sur `127.0.0.1:8765`. Ne change pas cette adresse pour exposer le service à Internet. Le navigateur peut demander une autorisation d'accès réseau local ou bloquer localhost selon ses paramètres. Ne partage jamais la clé locale ni tes identifiants de broker.

## Automatisation et sécurité
- Le détecteur de setups est expérimental et ne prouve pas la rentabilité. Il examine les bougies clôturées et peut proposer un scénario ; backtest et validation en démo indispensables.
- Le mode automatique couvre le rafraîchissement, l'analyse, le filtrage, les calculs, les alertes et le préremplissage de ticket. Toute exécution réelle conserve une confirmation humaine.
- L'envoi réel reste désactivé tant que `allow_live_orders` est `false`. Le pont applique des contrôles de risque, de spread, de stop, de volume et de marge.
- Le P&L journalier est calculé sur les deals clôturés depuis minuit UTC, et peut différer du jour de référence du broker.
- Les valeurs de contrat, tick size, tick value, commissions, swap, spread et slippage dépendent du symbole et du broker. Les cotations TradingView ne sont pas nécessairement identiques au Bid/Ask MT5.
- Aucun module ne garantit une session rentable ou l'absence de perte. Vérifier les règles officielles FTMO/Vantage et tester en compte démo avant tout ordre réel.

## Confidentialité
`bridge_config.local.json` contient la clé d'accès locale et les chemins de terminaux. Ne le téléverse jamais dans GitHub. Le journal web est stocké localement dans le navigateur ; exporte-le régulièrement.
