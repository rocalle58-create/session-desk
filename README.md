# Trading Performance Cockpit V5

Cockpit web personnel pour le scalping et le day trading, priorité Gold / SMC, avec profils FTMO et Vantage.

## Configuration retenue
- Autorité : **ASSIST**. Le cockpit conseille et vérifie ; la décision et l'exécution restent humaines.
- Signaux : **BOTH**. Pré-alerte de sweep puis confirmation par displacement, MSS et FVG.
- Risque de référence : **0,50 % maximum par trade** dans le calculateur. Ce plafond est un paramètre interne, pas une règle officielle FTMO ou Vantage.
- Aucun pont MT5, aucune connexion broker, aucun ordre automatique.

## Modules
- TradingView intégré : ticker et graphique interactif.
- Macro desk : calendrier économique TradingView et grille qualitative des facteurs macro (DXY, US 10Y, taux réels, Fed, régime risk-on/off, COT).
- Biais multi-timeframe Gold et DXY : M1, M5, M15, M30, H1, H4, D1 et W1.
- Corrélations glissantes de Pearson entre le DXY et les actifs importés, sur un timeframe sélectionné.
- Volatility monitor : ATR(14), ATR relatif à sa moyenne récente et régime de volatilité sur toutes les unités importées.
- Détecteur SMT intermarket sur pivots comparables et actifs configurables (DXY, Silver, EURUSD, GBPUSD).
- Radar en deux étapes : pré-alerte de sweep puis confirmation par displacement, MSS et FVG.
- Risk Guardian, ticket de calcul de lots, checklist pré-session, journal et sauvegarde locale complète.

## Données et limites
Le widget TradingView affiche le graphique et le calendrier, mais ne met pas ses chandeliers à disposition du JavaScript de cette page. Pour cette raison, l'analyse multi-timeframe, les corrélations, l'ATR, les SMT et le radar de signaux utilisent les fichiers OHLC CSV exportés depuis TradingView puis importés dans le cockpit.

Le moteur recalcule régulièrement les indicateurs sur les historiques importés, mais ce recalcul n'actualise pas les données de marché. Réimporte un CSV pour actualiser les séries. L'horodatage doit être cohérent entre les instruments pour les corrélations et SMT.

Les taux, la Fed, le positionnement COT et le régime de risque sont des entrées qualitatives à renseigner manuellement. Le calendrier TradingView est un widget externe : vérifie les chiffres, l'heure de Paris et les annonces auprès des sources officielles. Aucun flux macro fondamental en temps réel n'est prétendu.

Les corrélations varient et n'impliquent pas de causalité. Un SMT est une divergence potentielle, pas un signal autonome. Les seuils et règles sont heuristiques et doivent être validés par des tests historiques hors échantillon, avec spread, commissions et slippage.

## Données locales
Les journaux, réglages et historiques OHLC importés sont stockés dans le navigateur. Ils ne se synchronisent pas entre appareils. Utilise Exporter sauvegarde complète pour conserver journal, historiques et paramètres macro.

## Déploiement
GitHub Pages est publié depuis rocalle58-create/session-desk par le workflow .github/workflows/pages.yml.

Outil d'organisation et de contrôle, pas un conseil financier. Aucun indicateur, setup ou garde-fou ne garantit une session rentable.
