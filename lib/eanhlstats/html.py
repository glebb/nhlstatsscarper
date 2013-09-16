'''Nhl stats tool'''
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib2
from eanhlstats.model import Team, Player, get_player_from_db, get_team_from_db
from datetime import datetime
import eanhlstats.settings

TEAM_URL_PREFIX = "http://www.easportsworld.com/en_US/clubs/NHL14"
TEAM_URL_POSTFIX = "/overview"

MEMBERS_URL_PREFIX = "http://www.easportsworld.com/en_US/clubs/partial/NHL14"
MEMBERS_URL_POSTFIX = "/members-list"

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
    search_url += '&find[region]=&find[team_leagueId]=' + \
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

def get_content(url):
    '''Get html content of given url.
    untested copy/paste code'''
    content = None
    if url:
        try:
            url_handle = urllib2.urlopen(url, timeout=60)
            content = url_handle.read()
            url_handle.close()
        except IOError, error:
            print 'We failed to open "%s".' % url
            if hasattr(error, 'code'):
                print 'We failed with error code - %s.' % error.code
            elif hasattr(error, 'reason'):
                print "The error object has the following 'reason' attribute :"
                print error.reason
                print "This usually means the server doesn't exist,",
                print "is down, or we don't have an internet connection."
    return content


def get_team_overview_html(team_name):
    '''Return team overview html from ea server. Stores team data to db, 
    if not already found from there'''
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

def _find_stat_table_cells(html):
    stats_table = html.find('table', 
        {'class' : 'plain full-width nowrap less-padding no-margin'})
    return stats_table.findAll('td')

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

def _replace_space_with_plus(text):
    '''Fix arguments provided by pyfibot, to be used
    with TeamStatsParser'''
    temp = text.strip()
    temp = temp.replace(' ', '+')
    return temp
