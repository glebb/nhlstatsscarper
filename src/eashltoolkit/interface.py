"""Main interface for eanhlstats functionality"""
from operator import itemgetter

from eashltoolkit.html.team import get_team_overview_json, \
    find_team, get_results_url, \
    parse_results_data, find_teams
from eashltoolkit.html.players import parse_player_data, get_player_ids
from eashltoolkit.html.common import get_content, get_api_url, positions


def stats_of_player(players, player):
    """Pretty print for player stats"""
    temp = next((item for item in players if item['playername'] == player.upper()), None)
    stats = ""
    if temp:
        stats = \
            "%s %s GP:%s G:%s A:%s +/-:%s PIM:%s Hits:%s BS:%s S:%s S%%:%s GAA:%s SVP:%s" \
            % (positions[temp['position']], temp['playername'], temp['gamesplayed'],
               temp['skgoals'],
               temp['skassists'], temp['skplusmin'], temp['skpim'],
               temp['skhits'], temp['skbs'], temp['skshots'],
               temp['skshotpct'], temp['glgaa'], temp['glsavepct'])
    return stats


def get_ids(eaid):
    url = get_api_url(eaid, 'members')
    team_members_json = get_content(url)
    return get_player_ids(team_members_json)


def get_players(eaid, ids):
    postfix = 'members/' + ','.join(map(str, ids)) + '/stats'
    url = get_api_url(eaid, postfix)
    url = url.replace('clubs/' + eaid, '')
    players_json = get_content(url)
    return parse_player_data(players_json)


def sort_top_players(players, sort_by, limit=None, per_game=False):
    """Get all players for team. Refresh if needed from EA server.
    Returns None if not found"""
    for sub in players:
        for key in sub:
            is_numeric = False
            if key != 'playername' and key != 'firstname' and key != 'lastname':
                if type(sub[key]) is not int and _safe_cast(sub[key], float) and "." in sub[key]:
                    sub[key] = float(sub[key])
                elif type(sub[key]) is int or _safe_cast(sub[key], int) or sub[key] == '0':
                    sub[key] = int(sub[key])
                    if not key.endswith('pct'):
                        is_numeric = True
            if per_game and key == sort_by and is_numeric:
                sub[key] = float("%.2f" % (float(sub[key]) / float(sub['gamesplayed'])))

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


def find_team_with_stats(team_name):
    """Gets team stats from EA servers."""
    json = get_team_overview_json(team_name)
    if json and json != '[]' and json != '{"raw":[]}':
        return find_team(json)
    return None


def stats_of_team(teamdata):
    """Pretty print for team stats"""
    stats = ""
    if teamdata:
        stats = \
            "%s ID: %s GP: %s | %.1f%% | %s-%s-%s | AGF: %s | AGA: %s | Points: %s" \
            % (teamdata['team_name'],
               teamdata['eaid'],
               teamdata['games_played'],
               (float(teamdata['wins']) / float(teamdata['games_played'])) * 100,
               teamdata['wins'],
               teamdata['losses'],
               teamdata['overtime_losses'],
               teamdata['average_goals_for'],
               teamdata['average_goals_against'],
               teamdata['ranking'])
    return stats


def last_games(amount, team=None, eaid=None):
    """Pretty print results of last games for team"""
    temp = ""
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


def game_details(game_number, eaid):
    """last results for last games for team"""
    url = get_api_url(eaid, 'matches')
    json = get_content(url)
    index = game_number - 1
    games = parse_results_data(json, eaid)
    if index < len(games):
        return games[index]
    return None


def find_teams_by_abbreviation(abbreviation):
    """Find teams by abbreviaton"""
    return find_teams(abbreviation)


def pretty_print_teams(teams, amount):
    temp = ""
    for team in teams[0:amount]:
        temp += team['name'] + ', '
    return temp.strip()[:-1].strip()


def _safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except ValueError:
        return default
