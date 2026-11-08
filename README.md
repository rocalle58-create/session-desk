# Trading Performance Cockpit

Cockpit web personnel pour le scalping et le day trading, avec priorité Gold / SMC et profils FTMO et Vantage.

## Modules
- Graphique interactif TradingView intégré, ruban de cotations et sélection d'actif et d'unité de temps.
- Préparation de session et checklist.
- Market Radar et playbooks SMC.
- Risk Guardian, journal de trading, statistiques et export JSON.
- Profil FTMO ou Vantage sélectionnable dans l'interface.

## TradingView et cours
Le graphique et le ruban de cotations sont fournis par TradingView. Selon le symbole, le fournisseur et les droits de marché, les données peuvent être différées ou différentes des cotations de ton broker. TradingView est une référence visuelle : les valeurs du widget ne sont pas synchronisées avec le Bid/Ask, les positions ou le solde de FTMO/Vantage.

Vérifie toujours le prix, le spread et les spécifications du symbole sur ta plateforme broker avant de prendre une position. L'exécution des ordres reste manuelle sur FTMO ou Vantage. Ce projet ne se connecte pas à MT5 et ne transmet aucun ordre.

## Données et confidentialité
Les réglages et le journal sont conservés localement dans le navigateur. Ils ne sont pas automatiquement synchronisés entre appareils. Exporte régulièrement ton journal JSON pour conserver une sauvegarde.

## Déploiement
GitHub Pages est publié depuis rocalle58-create/session-desk par le workflow pages.yml.

Outil d'organisation et d'analyse, pas un conseil financier. Aucun indicateur, setup ou garde-fou ne garantit une session rentable.
