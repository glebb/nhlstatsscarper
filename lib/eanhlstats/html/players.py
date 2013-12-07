'''Player data parsing'''
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from eanhlstats.model import Player, get_player_from_db
from datetime import datetime
import eanhlstats.settings
from eanhlstats.html.common import get_content, PARTIAL_URL_PREFIX
import json

MEMBERS_URL_POSTFIX = "/members-list"


def get_player_ids(json_data):
    data = json.loads(json_data)
    temp = []
    data = data['raw'][0]
    for player in data.values():
        temp.append(player['blazeId'])
    return temp
        
def parse_player_data(json_data):
    data = json.loads(json_data)
    if 'raw' in data:
        return data['raw']
    return None

def _create_player(tdcells, team):
    player = None
    try:
        name = str(tdcells[1].div.a.string)
    except AttributeError:
        print "Parsing player stats failed"
    finally:
        player = get_player_from_db(name, team)
        
    if not player:
        player = Player()
        
    try:
        player.name = str(tdcells[1].div.a.string)
        player.goals = str(tdcells[3].string)
        player.assists = str(tdcells[4].string)
        player.points = str(tdcells[5].string)
        player.plusminus = str(tdcells[6].string)
        player.penalties = str(tdcells[7].string)
        player.power_play_goals = str(tdcells[8].string)
        player.short_handed_goals = str(tdcells[9].string)
        player.hits = str(tdcells[10].string)
        player.blocked_shots = str(tdcells[11].string)
        player.shots = str(tdcells[12].string)
        player.shooting_percentage = str(tdcells[13].string)
        player.team_eaid = team.eaid
        player.platform = eanhlstats.settings.SYSTEM
        player.modified = datetime.now()
    except AttributeError:
        print "Parsing player stats failed"
        
    return player
    
def refresh_player_data(team):
    data = get_content(PARTIAL_URL_PREFIX + eanhlstats.settings.SYSTEM + 
        "/" + team.eaid + MEMBERS_URL_POSTFIX)
    players = parse_player_data(team, data)
    if players:
        Player.delete().where(Player.team_eaid == team.eaid)
        for player in players:
            player.save()
