'''Team data parsing'''
# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from eanhlstats.model import Team, get_team_from_db
import eanhlstats.settings
from eanhlstats.html.common import get_content, PARTIAL_URL_PREFIX

TEAM_URL_PREFIX = "http://www.easportsworld.com/en_US/clubs/NHL14"


def create_search_url(team_name, use_abbreviation=False):
    '''Append team_name to Ea Sport Nhl search_url'''
    temp = _replace_space_with_plus(team_name)
    search_url = 'http://www.easportsworld.com/en_US/clubs/nhl14/search' + \
        '?find[name]='
    if not use_abbreviation:
        search_url += temp
    search_url += '&find[abbreviation]='
    if use_abbreviation:
        search_url += temp
    search_url += '&find[size]=' + \
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

def get_team_overview_html(team_name):
    '''Return team overview html from ea server. Stores team data to db, 
    if not already found from there'''
    TEAM_URL_POSTFIX = "/standings?type=overall"
    
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
    data = get_teams_from_search_page(html)
    if data:
        team_url = data[0]['url']
        team = _save(team_url, team_name)
        return team
    return None

def find_teams(abbreviation):
    search_url = create_search_url(abbreviation, True)
    html = get_content(search_url)
    teams = get_teams_from_search_page(html)
    if teams:
        save_teams_to_db(teams)
    return teams

def save_teams_to_db(teams):
    for data in teams:
        team_url = data['url']
        team_name = data['name']
        ea_id = _get_eaid_from_url(team_url)
        if Team.select().where(Team.eaid == ea_id).count() == 0:
            _save(team_url, team_name)

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

def _save(team_url, team_name):
    ea_id = _get_eaid_from_url(team_url)
    team = Team(name=team_name, platform=eanhlstats.settings.SYSTEM, 
        eaid=ea_id)
    team.save()
    return team

def _get_eaid_from_url(url):
    return url.split('/')[-2]
        
