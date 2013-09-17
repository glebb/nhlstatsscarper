'''Player data parsing'''
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from eanhlstats.model import Player, get_player_from_db
from datetime import datetime
import eanhlstats.settings
from eanhlstats.html.common import get_content

MEMBERS_URL_PREFIX = "http://www.easportsworld.com/en_US/clubs/partial/NHL14"
MEMBERS_URL_POSTFIX = "/members-list"

def parse_player_data(team, html):
    '''actual parsing, gets all the players in html
    as tr rows'''
    html = BeautifulSoup(html)
    members = []
    players = []
    try:
        member_table = html.find('table', 
            {'class' : 'styled full-width no-margin'}).tbody
        members = member_table.findAll('tr')
        for member in members:
            tdcells = member.findAll('td')
            player = _create_player(tdcells, team)
            players.append(player)
    except AttributeError:
        print "Parsing player stats failed"
    return players

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
        player.team_eaid = team.eaid
        player.platform = eanhlstats.settings.SYSTEM
        player.modified = datetime.now()
    except AttributeError:
        print "Parsing player stats failed"
        
    return player
    
def refresh_player_data(team):
    data = get_content(MEMBERS_URL_PREFIX + eanhlstats.settings.SYSTEM + 
        "/" + team.eaid + MEMBERS_URL_POSTFIX)
    players = parse_player_data(team, data)
    if players:
        Player.delete().where(Player.team_eaid == team.eaid)
        for player in players:
            player.save()
