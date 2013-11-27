'''Main interface for eanhlstats functionality'''
from eanhlstats.model import get_team_from_db, get_player_from_db, \
    get_players_from_db, Player
from eanhlstats.html.team import get_team_overview_html, \
    save_new_team_to_db, parse_team_standings_data, get_results_url, \
    parse_results_data, parse_last_game, find_teams, TEAM_URL_PREFIX

from eanhlstats.html.players import refresh_player_data
from eanhlstats.html.common import get_content, get_api_url
import eanhlstats.settings
from datetime import datetime
from peewee import DoesNotExist

def get_player(player_name, team):
    '''Get single Player data from db. Refresh if needed from EA server. 
    Returns None if not found'''
    player = None
    player = get_player_from_db(player_name, team)
    if not player or _needs_refresh(player):
        refresh_player_data(team)
        player = get_player_from_db(player_name, team)
    return player
        
def stats_of_player(player):
    '''Pretty print for player stats'''
    stats = ""
    if player:
        stats = \
            "%s G:%s A:%s +/-:%s PIM:%s Hits:%s BS:%s S:%s S%%:%s" \
            % (player.name, \
            player.goals, \
            player.assists, player.plusminus, player.penalties, \
            player.hits, player.blocked_shots, player.shots, \
            player.shooting_percentage)
    return stats
     
def get_players(team):
    '''Get all players for team. Refresh if needed from EA server. 
    Returns None if not found'''
    players = get_players_from_db(team)
    try:
        first = players.get()
    except DoesNotExist:
        first = None
    if not first or _needs_refresh(first):
        refresh_player_data(team)
        players = get_players_from_db(team)
    return players

def top_players(players, max_amount):
    '''Order a SelectQuery of players by score and return pretty print string. 
    max_amount specifies how many players there should be.'''
    temp = ""
    i = 1
    for player in players.order_by(Player.points.desc()).limit(max_amount):
        temp += "%s.%s (%s), " % (i, player.name, player.points)
        i += 1
    return temp.strip()[:-1]
     
def get_team(team_name):
    '''Get Team object from db. If team does not exist in local db
    does a query to EA servers and creates a new entry. Returns None
    in case of team does not exist or other error'''
    team = get_team_from_db(team_name)
    if not team:
        team = save_new_team_to_db(team_name)
    return team
              
def get_team_stats(team):
    '''Gets team stats from EA servers.'''
    if team:
        html = get_team_overview_html(team.name)    
        return parse_team_standings_data(html)
    return None

def stats_of_team(teamdata):
    '''Pretty print for team stats'''
    stats = ""
    if teamdata:
        stats = \
            "%s %s GP: %s | %.1f%% | %s-%s-%s | AGF: %s | AGA: %s | OR: %s" \
            % (teamdata['team_name'], \
            teamdata['region'], \
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
        temp += result + ' | '
    return temp.strip()[:-1].strip()

def last_game(eaid):
    '''Pretty print results of last games for team'''
    temp = ""
    url = get_api_url(eaid, 'matches?matches_returned=1')
    json = get_content(url)
    return parse_last_game(json, eaid)


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

