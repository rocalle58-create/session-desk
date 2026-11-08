# Trading Performance Cockpit v4

Cockpit personnel en validation assistée, pour scalping + day trading, priorité Gold et risque de référence plafonné à 0,50 % par trade.

## Fonctionnalités
- Dashboard de départ avec statuts WAIT / READY / LOCK et checklist pré-session.
- TradingView intégré : ticker multi-marchés, graphique et choix du symbole / timeframe.
- Sources de signaux BOTH : graphique TradingView (observation visuelle) + moteur de règles du cockpit (confirmations saisies manuellement).
- Trois setups SMC : Sweep + MSS + FVG, Trend continuation et SMT + confirmation.
- Calculateur de taille de position fondé sur l'équité, le stop, le tick size, le tick value, le lot step et les coûts.
- Risk Guardian : risque ouvert, budget disponible, limite journalière interne et verrou de session.
- Validation humaine du ticket, journal local, métriques en R et export JSON.
- Profils FTMO et Vantage, valeurs de départ modifiables manuellement.

## Utilisation
Ouvre https://rocalle58-create.github.io/session-desk/ dans Chrome ou Edge. Les widgets TradingView nécessitent Internet. Choisis l'actif, le timeframe et le compte ; mets à jour l'équité, la devise et les spécifications réelles du contrat auprès du broker.

## Limites importantes
- Aucun pont MT5, aucune connexion broker et aucun ordre envoyé par le site. L'exécution reste manuelle sur ta plateforme.
- Le widget TradingView est intégré, mais ses données OHLC ne sont pas accessibles au JavaScript du cockpit. Le moteur Cockpit évalue les conditions que tu coches ; il ne prétend pas détecter automatiquement les sweeps, MSS ou FVG depuis TradingView. Les deux sources sont côte à côte, pas fusionnées en un flux automatique.
- Les cotations TradingView peuvent être différées et différer du Bid/Ask d'exécution.
- Tick size, tick value, coûts et pas de lot doivent être vérifiés pour chaque symbole et broker. Les valeurs initiales du ticket sont des exemples.
- Les profils de comptes affichent des valeurs de départ modifiables ; le site ne lit pas le solde ni les règles officielles FTMO/Vantage.
- Le risque de 0,50 % est un plafond de référence interne, pas une promesse de rentabilité. Le journal est saisi manuellement et stocké dans le navigateur.
- STOP SESSION bloque les nouvelles validations dans le cockpit ; il ne ferme aucune position et ne remplace pas un stop placé côté broker.

## Données et sauvegarde
Les sessions et le journal restent dans le stockage local du navigateur. Exporte régulièrement le journal JSON.

## Publication
GitHub Pages publie la branche main. L'application compressée est découpée en dix fragments texte cockpit-v4-part-00.txt à cockpit-v4-part-09.txt, assemblés par index.html.
