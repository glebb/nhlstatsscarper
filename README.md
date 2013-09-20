# EA Sports Nhl 14 statistics Scraper for irc #

## Summary ##
 *  eanhlstats: python module to fetch and parse team & player stats from easports servers. (append lib to PYTHONPATH)
 *  pyfibot_module: module for pyfibot irc bot (https://github.com/lepinkainen/pyfibot), which uses eanhlstats package. Place inside modules folder of pyfibot.
 
## Examples ## 
<pre>
15:22:11 <@bodhi> .ts murohoki
15:22:23 < mhstatsbot> murohoki Europe 56-38-7 | OR: 129 | http://www.easportsworld.com/en_US/clubs/NHL14PS3/26/match-results

15:22:32 <@bodhi> .top murohoki
15:22:32 < mhstatsbot> 1.arielii (141), 2.HOLYDIVERS (115), 3.Noddactius (79), 4.Mr_Fagstrom (78), 5.qolazor (41)

15:22:25 <@bodhi> .ps bodhi-fin@murohoki
15:22:30 < mhstatsbot> bodhi-FIN G:4 A:3 +/-:5 PIM:6 Hits:21 BS:1 S:17

15:24:31 < bodhi> .find fin
15:24:34 < mhstatsbot> Finland Legends, xX  Finlandia  Xx, Germanys Finest, Leijonat, FINLAND, Kirvesrinnat, Swaggers
</pre>


## Bot commands ##
 .ts <team name>: Show Team Stats for team (always fetched from server)
 .ps <player_name@team>: show player stats from a specific team. Within single request data is cached for 5 minutes for the whole team, making following requests from the same team faster. 
 .switch: Switch between PS3 and Xbox 360 mode (can only fetch data from one at a time)
 .top <team name>: Show top 5 players from team.
 .find <team abbreviation>: Show max 10 team names using provided abbreviation.

## Install ##
 *  install & config pyfibot so it runs ok
 *  clone nhlstatsscraper repo
 *  copy or link pyfibot_module/module_nhl_stats.py to pyfibot/modules folder
 *  add nhlstatsscraper/lib to PYTHONPATH. You can modify pyfibot run.sh and add export statement as the first line: export PYTHONPATH=$PYTHONPATH:/folder/to/nhlstatsscraper/lib
 *  From eanhlstats.settings set whether you are interested in PS3 or XBX statistics by default. You can also change the default cache time for player stats (so they are not constantly fetched from servers).

For using outside pyfibot context, check interface.py on how to use this thing.	

Run tests with ./runtests.sh

Requirements:
 *  Peewee
 *  BeautifulSoup
 
 Dev:
 *  Specloud
 *  Mock
 *  coverage