from eanhlstats.model import *
from eanhlstats.html import get_team_overview_html, save_new_team_to_db, get_content, parse_team_overview_data, MEMBERS_URL_PREFIX, MEMBERS_URL_POSTFIX, parse_player_data
from peewee import DoesNotExist
import eanhlstats.settings
from datetime import datetime

def get_team(team_name):
    '''Get Team object from db. If team does not exist in local db
    does a query to EA servers and creates a new entry. Returns None
    in case of team does not exist or other error'''
    team = get_team_from_db(team_name)
    if not team:
        team = save_new_team_to_db(team_name)
    return team
    
def get_player(player_name, team):
    '''Get Player data from db. Refresh if needed from EA server. Returns None if not found'''
    player = None
    player = get_player_from_db(player_name, team)
    if not player or ((datetime.now() - player.modified).seconds / 60 > eanhlstats.settings.CACHE_TIME):
        _refresh_player_data(team)
        player = get_player_from_db(player_name, team)
    return player
        
def get_team_stats(team):
    '''Gets team stats from EA servers.'''
    if team:
        html = get_team_overview_html(team.name)    
        return parse_team_overview_data(html)
    return None
    
def stats_of_player(player):
    '''Pretty print for player stats'''
    stats = ""
    if player:
        stats = \
            "%s G:%s A:%s +/-: %s PIM: %s Hits: %s BS: %s S: %s" \
            % (player.name, \
            player.goals, \
            player.assists, player.plusminus, player.penalties, \
            player.hits, player.blocked_shots, player.shots)
    return stats

def stats_of_team(teamdata):
    '''Pretty print for team stats'''
    stats = ""
    if teamdata:
        stats = \
            "%s %s %s | OR: %s|" \
            % (teamdata['team_name'], \
            teamdata['region'], \
            teamdata['club_record'], \
            teamdata['ranking'])
    return stats


def _refresh_player_data(team):
    data = get_content(MEMBERS_URL_PREFIX + team.eaid + MEMBERS_URL_POSTFIX)
    players = parse_player_data(team, data)
    for player in players:
        player.save()
