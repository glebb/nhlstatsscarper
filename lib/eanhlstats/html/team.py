'''Team data parsing'''
# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from eanhlstats.model import Team, get_team_from_db
import eanhlstats.settings
from eanhlstats.html.common import get_content, PARTIAL_URL_PREFIX

def create_search_url(team_name):
    '''Append team_name to Ea Sport Nhl search_url'''
    temp = _replace_space_with_plus(team_name)
    search_url = 'http://www.easportsworld.com/en_US/clubs/nhl14/search' + \
        '?find[name]='
    search_url += temp
    search_url += '&find[abbreviation]=&find[size]=' + \
        '&find[acceptJoinRequest]=&find[public]=&find[lang]=' + \
        '&find[platform]='
    platform = "360" if eanhlstats.settings.SYSTEM == "XBX" \
        else eanhlstats.settings.SYSTEM
    search_url += platform
    search_url += '&find[region]='
    if eanhlstats.settings.REGION:
        search_url += str(eanhlstats.settings.REGION)
    search_url += '&find[team_leagueId]=' + \
        '&find[teamId]=&find[active]=true&do-search=submit'
    return search_url

def parse_team_overview_data(html):
    '''Do the parsing of html. After this method is finished
    individual data can be fetched e.g club_record()'''
    html = BeautifulSoup(html)
    data = {}
    try:
        team_header = html.find('div', {'class' : 'main-club-header'})
        data['team_name'] = team_header.h1.a.string
        stat_cells = _find_stat_table_cells(html)
        data['club_record'] = stat_cells[0].span.string.replace(' ', '')
        data['region'] = stat_cells[1].string.replace("Region: ", "")
        data['ranking'] = \
            stat_cells[2].string.replace("Overall Ranking: ", "")
        return data
    except AttributeError:
        print "Parsing team stats failed"
        return None
    
def get_team_url(html, number=1):
    '''Get the url for team overview, param number defines which url to get,
    in case there are more than one. Defaults always to first.'''
    html = BeautifulSoup(html)
    try:
        containing_table = html.find('table', 
            {'class' : 'styled full-width'})
        links = containing_table.tbody.findAll('h4')
        postfix = links[number-1].a['href']
    except AttributeError:
        return None
    except IndexError:
        return None

    prefix = 'http://www.easportsworld.com'
    return prefix + postfix

def get_team_overview_html(team_name):
    '''Return team overview html from ea server. Stores team data to db, 
    if not already found from there'''
    TEAM_URL_PREFIX = "http://www.easportsworld.com/en_US/clubs/NHL14"
    TEAM_URL_POSTFIX = "/overview"
    
    content = None
    team = get_team_from_db(team_name)
    if team:
        content = get_content(TEAM_URL_PREFIX + eanhlstats.settings.SYSTEM + 
            "/" + team.eaid + TEAM_URL_POSTFIX)
    else:
        team = save_new_team_to_db(team_name)
        if team:
            content = get_content(TEAM_URL_PREFIX + 
            eanhlstats.settings.SYSTEM + "/" + team.eaid + TEAM_URL_POSTFIX)
    return content

def save_new_team_to_db(team_name):
    '''Does a search query on Ea servers and stores team data (eaid)
    to db. Returns None if team is not found.'''
    search_url = create_search_url(team_name)
    html = get_content(search_url)
    team_url = get_team_url(html)
    if team_url:
        ea_id = team_url.split('/')[-2]
        team = Team(name=team_name, platform=eanhlstats.settings.SYSTEM, 
            eaid=ea_id)
        team.save()
        return team
    return None

def get_results_url(eaid):
    temp = PARTIAL_URL_PREFIX + eanhlstats.settings.SYSTEM + '/' + eaid + '/' + 'match-results?type=all'
    return temp
    
def parse_results_data(html):
    data = []
    soup = BeautifulSoup(html)
    try:
        table = soup.find('table', {'class' : 'styled full-width'})
        rows = table.findAll('tr', {'class' : 'black'})
    except AttributeError:
        return data
    for row in rows:
        try:
            result = row.findAll('td')[2].div.string.replace(' ','')
            team = row.findAll('td')[4].div.a.string
            data.append(_won_or_lost(result) + ' ' + result + ' against ' +team)
        except AttributeError:
            pass
    return data
    
def _won_or_lost(result):
    home, away = result.split('-')
    return "Won" if int(home) > int(away) else "Lost"

def _replace_space_with_plus(text):
    '''Fix arguments provided by pyfibot, to be used
    with TeamStatsParser'''
    temp = text.strip()
    temp = temp.replace(' ', '+')
    return temp
    
def _find_stat_table_cells(html):
    stats_table = html.find('table', 
        {'class' : 'plain full-width nowrap less-padding no-margin'})
    return stats_table.findAll('td')

