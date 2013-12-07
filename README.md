## EA Sports Nhl 14 statistics Scraper for irc ##

### Summary ###
 *  eanhlstats: python module to fetch and parse team & player stats from easports servers. (append lib to PYTHONPATH)
 *  pyfibot_module: module for pyfibot irc bot (https://github.com/lepinkainen/pyfibot), which uses eanhlstats package. Place inside modules folder of pyfibot.
 
### Examples ###
<pre>
15:22:11 <@bodhi> .ts murohoki
15:22:23 < mhstatsbot> murohoki Europe 56-38-7 | OR: 129 | http://www.easportsworld.com/en_US/clubs/NHL14PS3/26/match-results

15:22:32 <@bodhi> .top skpoints
15:22:32 < mhstatsbot> 1.arielii (141), 2.HOLYDIVERS (115), 3.Noddactius (79), 4.Mr_Fagstrom (78), 5.qolazor (41)

15:22:25 <@bodhi> .ps bodhi-fin
15:22:30 < mhstatsbot> bodhi-FIN G:4 A:3 +/-:5 PIM:6 Hits:21 BS:1 S:17

15:24:31 < bodhi> .find fin
15:24:34 < mhstatsbot> Finland Legends, xX  Finlandia  Xx, Germanys Finest, Leijonat, FINLAND, Kirvesrinnat, Swaggers
</pre>


### Bot commands ###
<pre>
 .ts <team name>: Show Team Stats for team (always fetched from server)
 .ps <player_name>: show player stats from a default team. 
 .switch: Switch between PS3 and Xbox 360 mode (can only fetch data from one at a time)
 .top <value>: Show top 10 players from team, sorted by value (e.g. skpoints)
 .find <team abbreviation>: Show max 10 team names using provided abbreviation.
 .trackresults: Enable tracking results for default time. Polls the servers and when finding updated results broadcasts on channel
 .results: show last 5 games for deafult team
 .game <nr>: Display summary and default team points for selected game (as list by .results) 
</pre>

### Install ###
 *  install & config pyfibot so it runs ok
 *  clone nhlstatsscraper repo
 *  copy or link pyfibot_module/module_nhl_stats.py to pyfibot/modules folder
 *  add nhlstatsscraper/lib to PYTHONPATH. You can modify pyfibot run.sh and add export statement as the first line: export PYTHONPATH=$PYTHONPATH:/folder/to/nhlstatsscraper/lib
 *  From eanhlstats.settings set whether you are interested in PS3 or XBOX statistics by default. Also set default team eaid (used by many commands)

 Run tests with ./runtests.sh

### Requirements ###
 *  BeautifulSoup
 *  pytz
 *  python-dateutil
 *  Specloud (dev)
 *  Mock (dev)
 *  coverage (dev)

For using outside pyfibot context, check interface.py and tests on how to use this thing.	
