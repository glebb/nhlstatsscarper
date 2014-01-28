"""Team data parsing"""
# -*- coding: utf-8 -*-
import json

from BeautifulSoup import BeautifulSoup

import eanhlstats.settings
from eanhlstats.html.common import get_content, get_api_url, positions


def create_search_url(team_abbreviation):
    """Use old easports page for finding teams by abbreviation"""
    temp = _replace_space_with_plus(team_abbreviation)
    search_url = 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]='
    search_url += '&find[abbreviation]=' + temp
    search_url += '&find[size]=' + \
                  '&find[acceptJoinRequest]=&find[public]=&find[lang]=' + \
                  '&find[platform]='
    platform = "360" if eanhlstats.settings.SYSTEM == "XBOX" \
        else eanhlstats.settings.SYSTEM
    search_url += platform
    search_url += '&find[region]='
    if eanhlstats.settings.REGION:
        search_url += str(eanhlstats.settings.REGION)
    search_url += '&find[team_leagueId]=' + \
                  '&find[teamId]=&find[active]=true&do-search=submit'
    return search_url


def find_team(json_data):
    """Convert Json to simpler dict"""
    data = {}

    temp = json.loads(json_data)

    data['eaid'] = temp['raw'].keys()[0]

    temp = temp['raw'].values()[0]

    data['team_name'] = temp['name']
    data['club_record'] = temp['wins'] + '-' + temp['losses'] + '-' + temp['otl']
    data['ranking'] = temp['currentPoints']
    data['games_played'] = str(int(temp['wins']) + int(temp['losses']) + int(temp['otl']))
    data['wins'] = temp['wins']
    data['losses'] = temp['losses']
    data['overtime_losses'] = temp['otl']
    data['average_goals_for'] = "%.2f" % (float(temp['goals']) / float(data['games_played']))
    data['average_goals_against'] = "%.2f" % (float(temp['goalsAgainst']) / float(data['games_played']))

    return data


def get_teams_from_search_page(html):
    """Get the url for team overview.
    @rtype : list
    """
    html = BeautifulSoup(html)
    prefix = 'http://www.easportsworld.com'
    items = []
    try:
        containing_table = html.find('table',
                                     {'class': 'styled full-width'})
        links = containing_table.tbody.findAll('h4')
        for link in links:
            item = {'url': prefix + link.a['href'].replace('overview', 'standings?type=overall'), 'name': link.a.string}
            items.append(item)
    except (AttributeError, IndexError):
        pass

    return items


def get_team_overview_json(team_name):
    """Return team overview from ea server. Stores team data to db,
    if not already found from there"""
    content = get_content('http://www.easports.com/iframe/nhl14proclubs/api/platforms/' + \
                          eanhlstats.settings.SYSTEM + '/clubsComplete/' + _replace_space_with_url_encode(team_name))
    return content


def find_teams(abbreviation):
    search_url = create_search_url(abbreviation)
    temp = []
    html = get_content(search_url)
    teams = get_teams_from_search_page(html)
    if not teams:
        return None
    for data in teams:
        team = {'url': data['url'], 'name': data['name'], 'ea_id': _get_eaid_from_url(data['url'])}
        temp.append(team)
    return temp


def get_results_url(eaid):
    return get_api_url(eaid, 'matches')


def parse_results_data(json_data, eaid):
    """Get results data from json"""
    data = json.loads(json_data)
    temp = {}
    if len(data) > 0:
        data = data['raw']
        for game in data.keys():
            timestamp = data[game]['timestamp']
            result = None
            team = None
            players = ""
            for teamid in data[game]['clubs'].keys():
                if teamid == eaid:
                    result = data[game]['clubs'][teamid]['scorestring']
                    for player in data[game]['players'][teamid].keys():
                        players += positions[data[game]['players'][teamid][player]['position']] + ' '
                        players += data[game]['players'][teamid][player]['details']['personaName']
                        players += ' ' + data[game]['players'][teamid][player]['skgoals'] + '+'
                        players += data[game]['players'][teamid][player]['skassists']
                        if positions[data[game]['players'][teamid][player]['position']] == "G":
                            players += ' ' + data[game]['players'][teamid][player]['glsaves'] + '/'
                            players += data[game]['players'][teamid][player]['glshots'] + ' '
                            players += data[game]['players'][teamid][player]['glsavepct'] + '%'
                        players += ', '
                    continue
                team = data[game]['clubs'][teamid]['details']['name']
            if result and team:
                temp_game = {'summary': _won_or_lost(result) + ' ' + result + ' against ' + team,
                             'when': data[game]['timeAgo']}
                players = players.strip()[:-1]
                temp_game['players'] = players
                temp[timestamp] = temp_game
    results = []
    for result in sorted(temp.keys()):
        results.insert(0, temp[result])
    return results


def _won_or_lost(result):
    home, away = result.split('-')
    return "Won" if int(home) > int(away) else "Lost"


def _replace_space_with_plus(text):
    """Fix arguments provided by pyfibot, to be used
    with TeamStatsParser"""
    temp = text.strip()
    temp = temp.replace(' ', '+')
    return temp


def _replace_space_with_url_encode(text):
    """Fix arguments provided by pyfibot, to be used
    with TeamStatsParser"""
    temp = text.strip()
    temp = temp.replace(' ', '%20')
    return temp


def _get_eaid_from_url(url):
    return url.split('/')[-2]
        
