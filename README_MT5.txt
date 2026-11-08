TRADING PERFORMANCE COCKPIT — CONNEXION MT5 EN LECTURE SEULE

PRÉREQUIS
- Windows 10/11 64 bits.
- MT5 desktop installé et connecté à FTMO ou Vantage.
- Python 3.11 ou 3.12 64 bits depuis python.org.

INSTALLATION
1. Télécharge install_mt5_bridge.bat depuis ce dépôt et double-clique dessus.
2. Le dossier local est %USERPROFILE%\TradingPerformanceCockpit\MT5Bridge.
3. Ouvre MT5 et connecte-toi à ton compte FTMO ou Vantage.
4. Lance start_mt5_bridge.bat. La fenêtre noire affiche une clé API locale : copie-la et laisse cette fenêtre ouverte.

CONNEXION AU COCKPIT
1. Ouvre https://rocalle58-create.github.io/session-desk/
2. Dans MT5 Live Feed, garde http://127.0.0.1:8765.
3. Colle la clé affichée dans la fenêtre locale.
4. Sélectionne le profil qui correspond au compte actuellement ouvert dans MT5, puis clique Connecter MT5.
5. Autorise, si demandé, l'accès du navigateur au réseau local.

FTMO ET VANTAGE
Un seul terminal alimente le cockpit à la fois. Si les deux terminaux MT5 sont installés, modifie bridge_config.local.json pour renseigner les chemins exacts vers terminal64.exe et le server_hint de chacun des comptes. Pour trouver le chemin, clic droit sur le raccourci MT5 > Propriétés > Cible. Le server_hint doit correspondre au serveur affiché dans MT5.
Le pont réutilise la session déjà ouverte dans MT5 : ne mets aucun mot de passe dans le fichier JSON.

SYMBOLES
Les noms dépendent du broker (XAUUSD, GOLD, XAUUSD.a, etc.). Le champ Gold doit reprendre exactement le nom de Market Watch. Les actifs comparatifs peuvent être laissés vides si le broker ne les propose pas.

SÉCURITÉ
- Le pont écoute uniquement sur 127.0.0.1 ; il n'est pas accessible depuis Internet.
- La clé API est créée localement dans bridge_config.local.json. Ne la partage pas et ne publie jamais le fichier local.
- Lecture seule : aucune route d'envoi d'ordre, de modification de SL/TP ou de fermeture de position.
- Le point d'accès /api/macro récupère des séries publiques FRED (US 10Y nominal/réel, taux effectif Fed, CPI et Core PCE). Ce sont des observations macro publiées, pas des cotations temps réel. Actualisation du cache local : 15 minutes.
- Les séries sont téléchargées depuis les exports CSV des graphiques FRED ; ce mécanisme peut évoluer côté fournisseur. Le cockpit affiche les dates d'observation et les erreurs éventuelles.
- L'affichage macro comporte la mention FRED requise : le produit n'est ni approuvé ni certifié par la Federal Reserve Bank of St. Louis.
- DXY reste automatique uniquement si le symbole DXY existe chez le broker et est renseigné dans la correspondance des symboles. Le COT et le régime risk-on/off restent à valider manuellement.
- Les données du compte sont lues sur le PC et affichées dans ton navigateur.
- Le P&L journalier fourni est calculé depuis minuit UTC ; les limites broker/prop firm peuvent avoir un autre découpage et inclure le flottant.
- Le cockpit et le pont ne garantissent aucun résultat de trading.
