## EASHL toolkit for pyfibot ##

### Summary ###
EASHL toolkit provides a Python API and pyfibot module to fetch data from EA Sports servers regarding EASHL teams and players.
 
### Examples (pyfibot commands) ###
<pre>
22:46:24 <bodhi> .ts murohoki
22:46:25 <mhstatsbot> murohoki ID: 26 GP: 1171 | 60.5% | 708-370-93 | AGF: 2.90 | AGA: 2.32 | Points: 4896
22:46:26 <mhstatsbot> Won 4 - 1 against Ruttumunat Ry (1 hour ago) | LW arielii 1+0, D bodhi-FIN 0+1, D Noddactius 1+1, RW JohnAbruzzzi_ 0+1, C Lionite 2+1

22:52:00 <bodhi> .results murohoki
22:52:02 <mhstatsbot> Won 4 - 1 against Ruttumunat Ry (1 hour ago) | Won 4 - 1 against HC No Onhan Se Siella (2 hours ago) | Won 5 - 2 against HC PIGLET (2 hours ago) | Lost 2 - 6 against CZECHSTRIKERS (2 days ago) | Won 3 - 0 against Pulphockey (2 days ago)

15:22:32 <@bodhi> .top skpoints
15:22:32 < mhstatsbot> 1.arielii (141), 2.HOLYDIVERS (115), 3.Noddactius (79), 4.Mr_Fagstrom (78), 5.qolazor (41)

22:49:41 <bodhi> top_pg skpoints
22:49:42 <mhstatsbot> 1. MONTTUPOMO LIUKUMIINA (2.17), 2. KELLOGSIN TONYTIIKERI (2.0), 3. GAYLORD FOCKER (1.81), 4. JOHN VON ALBATROSS (1.75), 5. SKIGE KAAKELI (1.65), 6. TEEMU SELANNE (1.59), 7. VLADIMIR MALAKHOV (1.48), 8. HILPEA ROLLI (1.34), 9. ERIK SIXTY-FIVE (1.1), 10. NODDY NODDYNEN (0.98), 11. TEPPO WINNIPEG (0.69), 12. JIRI SLEGR (0.62)

22:47:17 <bodhi> .ps teppo winnipeg
22:47:18 <mhstatsbot> D TEPPO WINNIPEG GP:400 G:85 A:190 +/-:119 PIM:564 Hits:1217 BS:112 S:718 S%:11.8 GAA:0.00 SVP:0.000

15:24:31 < bodhi> .find fin
15:24:34 < mhstatsbot> Finland Legends, xX  Finlandia  Xx, Germanys Finest, Leijonat, FINLAND, Kirvesrinnat, Swaggers

22:48:32 <bodhi> .game 5
22:48:33 <mhstatsbot> Won 3 - 0 against Pulphockey (2 days ago) | D tidzan666 0+1, D Lionite 0+0, C Mr_Fagstrom 3+0, LW AlfrdJKwk 0+2, RW Malcowich84 0+1
</pre>


### Bot commands ###
<pre>
 .ts [team name]: Show Team Stats for team
 .ps [player_name]: Show player stats from a default team. 
 .switch: Switch between PS3 and Xbox 360 mode (can only fetch data from one at a time)
 .top [value]: Show top players from team, sorted by value (e.g. skpoints)
 .top_pg Show top players from team, sorted by value (e.g. skpoints) - per game
 .find [team abbreviation]: Show max 10 team names using provided abbreviation. If only one is found, automatically shows Team Stats
 .trackresults: Enable Polling match results from server. Will check the data every 2 minutes and broadcast the latest result to channel (if different from previous)
 .results: Show last 5 game results for default team
 .game [nr]: Display summary and default team points for selected game (as list by .results) 
</pre>

### Install ###
 *  install & config pyfibot so it runs ok
 *  clone the repo
 *  copy or link pyfibot_module/module_nhl_stats.py to pyfibot/modules folder
 *  add module to PYTHONPATH. You can modify pyfibot run.sh and add export statement as the first line: export PYTHONPATH=$PYTHONPATH:/folder/to/module
 *  From eashltoolkit.settings set whether you are interested in PS3 or XBOX statistics by default. Also set default team eaid (used by many commands)

 Run tests with ./runtests.sh

### Requirements ###
 *  BeautifulSoup
 *  Twisted (for bot)
 *  Specloud (dev)
 *  Mock (dev)
 *  coverage (dev)

For using outside pyfibot context, check interface.py and tests on how to use this thing.	
