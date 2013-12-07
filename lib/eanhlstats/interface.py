'''Main interface for eanhlstats functionality'''
from eanhlstats.model import get_team_from_db, get_player_from_db, \
    get_players_from_db, Player
from eanhlstats.html.team import get_team_overview_json, \
    save_new_team_to_db, find_team, get_results_url, \
    parse_results_data, find_teams, TEAM_URL_PREFIX
    
from operator import itemgetter

from eanhlstats.html.players import parse_player_data, get_player_ids
from eanhlstats.html.common import get_content, get_api_url
import eanhlstats.settings
from datetime import datetime
from peewee import DoesNotExist

def stats_of_player(players, player):
    '''Pretty print for player stats'''
    temp = next((item for item in players if item['playername'] == player), None)
    stats = ""
    if temp:
        stats = \
            "%s GP:%s G:%s A:%s +/-:%s PIM:%s Hits:%s BS:%s S:%s S%%:%s" \
            % (temp['playername'], temp['totalgp'], \
            temp['skgoals'], \
            temp['skassists'], temp['skplusmin'], temp['skpim'], \
            temp['skhits'], temp['skbs'], temp['skshots'], \
            temp['skshotpct'])
    return stats
     
def get_ids(eaid):
    url = get_api_url(eaid, 'members')
    team_members_json = get_content(url)
    return get_player_ids(team_members_json)
    
def get_players(eaid, ids):
    postfix = 'members/' + ','.join(map(str, ids)) + '/stats'
    url = get_api_url(eaid, postfix)
    players_json = get_content(url)
    return parse_player_data(players_json)

    
def sort_top_players(players, sort_by, limit=None):
    '''Get all players for team. Refresh if needed from EA server. 
    Returns None if not found'''
    for sub in players:
        for key in sub:
            if key != 'playername' and key != 'firstname' and key != 'lastname':
                if not isinstance(sub[key], int) and "." in sub[key]:
                    sub[key] = float(sub[key])    
                else:
                    sub[key] = int(sub[key])    
    try:
        temp = sorted(players, key=itemgetter(sort_by), reverse=True)
    except KeyError:
        return None
    string = ""
    i = 1
    if limit:
        temp = temp[0:limit]

    for player in temp:
        string += "%s. %s (%s), " % (i, player['playername'], player[sort_by])
        i += 1
    return string.strip()[:-1]

def top_players(players, max_amount):
    '''Order a SelectQuery of players by score and return pretty print string. 
    max_amount specifies how many players there should be.'''
    temp = ""
    i = 1
    for player in players.order_by(Player.points.desc()).limit(max_amount):
        temp += "%s. %s (%s), " % (i, player.name, player.points)
        i += 1
    return temp.strip()[:-1]
                   
def find_team_with_stats(team_name):
    '''Gets team stats from EA servers.'''
    json = get_team_overview_json(team_name)
    if json and json != '[]' and json != '{"raw":[]}':    
        return find_team(json)
    return None

def stats_of_team(teamdata):
    '''Pretty print for team stats'''
    stats = ""
    if teamdata:
        stats = \
            "%s GP: %s | %.1f%% | %s-%s-%s | AGF: %s | AGA: %s | Points: %s" \
            % (teamdata['team_name'], \
            teamdata['games_played'], \
            (float(teamdata['wins']) / float(teamdata['games_played'])) * 100, \
            teamdata['wins'], \
            teamdata['losses'], \
            teamdata['overtime_losses'], \
            teamdata['average_goals_for'], \
            teamdata['average_goals_against'], \
            teamdata['ranking'])
    return stats

def last_games(amount, team=None, eaid=None):
    '''Pretty print results of last games for team'''
    temp = ""
    today = datetime.today()
    if team:
        teamid = team.eaid
    elif eaid:
        teamid = eaid
    else:
        return None
    url = get_results_url(teamid)
    html = get_content(url)
    results = parse_results_data(html, teamid)
    for result in results[0:amount]:
        temp += result['summary'] + ' (' + result['when'] + ')' + ' | '
    return temp.strip()[:-1].strip()

def last_game(eaid):
    '''Pretty print results of last games for team'''
    url = get_api_url(eaid, 'matches?matches_returned=1')
    json = get_content(url)
    temp = parse_results_data(json, eaid)[0]
    return temp['summary'] + ' (' + temp['players'] + ')'

def game_details(game_number, eaid):
    '''Pretty print results of last games for team'''
    url = get_api_url(eaid, 'matches')
    json = get_content(url)
    index = game_number - 1
    games = parse_results_data(json, eaid)
    if index < len(games):
        return games[index]
    return None

def find_teams_by_abbreviation(abbreviation, amount):
    '''Find teams by abbreviaton'''
    return find_teams(abbreviation)
    
def pretty_print_teams(teams, amount):
    temp = ""
    for team in teams[0:amount]:
        temp += team.name + ', '
    return temp.strip()[:-1].strip()
    

def results_url(team):
    return TEAM_URL_PREFIX + eanhlstats.settings.SYSTEM + '/' + team.eaid + '/match-results'

    
def _needs_refresh(player):
    return ((datetime.now() - player.modified).seconds / 60 > 
        eanhlstats.settings.CACHE_TIME)

