'''Team data parsing'''
# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from eanhlstats.model import Team, get_team_from_db
import eanhlstats.settings
from eanhlstats.html.common import get_content, get_api_url
import datetime
import time
import pytz
from dateutil import parser
import json

TEAM_URL_PREFIX = "http://www.easportsworld.com/en_US/clubs/NHL14"
EET = pytz.timezone('Europe/Helsinki')
TARGET_TZ =  pytz.timezone('US/Pacific')


def create_search_url(team_abbreviation):
    '''Use old easports page for finding teams by abbreviation'''
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

def parse_team_standings_data(html):
    '''Do the parsing of html.'''
    return None

def find_team(json_data):
    '''Convert Json to simpler dict'''
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
    '''Get the url for team overview.'''
    html = BeautifulSoup(html)
    prefix = 'http://www.easportsworld.com'
    items = []
    try:
        containing_table = html.find('table', 
            {'class' : 'styled full-width'})
        links = containing_table.tbody.findAll('h4')
        for link in links:
            item = {}
            item['url'] = postfix = prefix + link.a['href'].replace('overview', 'standings?type=overall')
            item['name'] = link.a.string
            items.append(item)
    except (AttributeError, IndexError):
        return None

    return items

def get_team_overview_json(team_name):
    '''Return team overview from ea server. Stores team data to db, 
    if not already found from there'''
    content = None
    content = get_content('http://www.easports.com/iframe/nhl14proclubs/api/platforms/'+ \
        eanhlstats.settings.SYSTEM + '/clubsComplete/' + _replace_space_with_url_encode(team_name))
    return content

def save_new_team_to_db(team_name):
    '''Does a search query on Ea servers and stores team data (eaid)
    to db. Returns None if team is not found.'''
    search_url = create_search_url(team_name)
    html = get_content(search_url)
    data = get_teams_from_search_page(html)
    if data:
        team_url = data[0]['url']
        team = _save(team_url, team_name)
        return team
    return None

def find_teams(abbreviation):
    search_url = create_search_url(abbreviation)
    temp = {}
    
    html = get_content(search_url)
    teams = get_teams_from_search_page(html)
    if teams:
        temp = save_teams_to_db(teams)
        return temp
    return None

def save_teams_to_db(teams):
    temp = []
    for data in teams:
        team_url = data['url']
        team_name = data['name']
        ea_id = _get_eaid_from_url(team_url)
        team = Team.select().where(Team.eaid == ea_id)
        if team.count() == 0:
            team = _save(team_url, team_name)
        else:
            team = team.get()
        temp.append(team)
    return temp

def get_results_url(eaid):
    return get_api_url(eaid, 'matches')
    
def parse_results_data(json_data, eaid):
    '''Get results data from json'''
    data = json.loads(json_data)
    temp = {}
    if len(data) > 0:
        data = data['raw']
        for game in data.keys():
            timestamp = data[game]['timestamp']
            result = None
            for teamid in data[game]['clubs'].keys():
                if teamid == eaid:
                    result = data[game]['clubs'][teamid]['scorestring']
                    continue
                team = data[game]['clubs'][teamid]['details']['name']
            if result:
                temp[timestamp] = _won_or_lost(result) + ' ' + result + ' against ' + team + ' (' + data[game]['timeAgo'] + ')' 

    results = []
    for result in sorted(temp.keys()):
        results.insert(0, temp[result])
    return results

def parse_last_game(json_data, eaid):
    data = json.loads(json_data)
    temp = {}
    if len(data) > 0:
        data = data['raw']
        players = "("
        result = None
        team = None
        for game in data.keys():
            for teamid in data[game]['clubs'].keys():
                if teamid == eaid:
                    result = data[game]['clubs'][teamid]['scorestring']
                    print result
                    for player in data[game]['players'][teamid].keys():
                        players += data[game]['players'][teamid][player]['details']['personaName']
                        players += ' ' + data[game]['players'][teamid][player]['skgoals'] + '+'
                        players += data[game]['players'][teamid][player]['skassists'] + ', '
                else:
                    team = data[game]['clubs'][teamid]['details']['name']
                    players = players.strip()[:-1] + ')'
            if result:
                return _won_or_lost(result) + ' ' + result + ' against ' + team + ' ' + players
    
def _won_or_lost(result):
    home, away = result.split('-')
    return "Won" if int(home) > int(away) else "Lost"

def _replace_space_with_plus(text):
    '''Fix arguments provided by pyfibot, to be used
    with TeamStatsParser'''
    temp = text.strip()
    temp = temp.replace(' ', '+')
    return temp

def _replace_space_with_url_encode(text):
    '''Fix arguments provided by pyfibot, to be used
    with TeamStatsParser'''
    temp = text.strip()
    temp = temp.replace(' ', '%20')
    return temp

    
def _find_stat_table_cells(html):
    stats_table = html.find('table', 
        {'class' : 'plain full-width nowrap less-padding no-margin'})
    return stats_table.findAll('td')

def _save(team_url, team_name):
    ea_id = _get_eaid_from_url(team_url)
    team = Team(name=team_name, platform=eanhlstats.settings.SYSTEM, 
        eaid=ea_id)
    team.save()
    return team

def _get_eaid_from_url(url):
    return url.split('/')[-2]
        
