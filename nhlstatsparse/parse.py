'''Nhl stats tool'''
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib2
from nhlstatsparse.db import Team, Player
from datetime import datetime
from peewee import DoesNotExist

SYSTEM = "PS3" #Alternatively XBX

TEAM_URL_PREFIX = "http://www.easportsworld.com/en_US/clubs/NHL14" + SYSTEM + "/"
TEAM_URL_POSTFIX = "/overview"

MEMBERS_URL_PREFIX = "http://www.easportsworld.com/en_US/clubs/partial/NHL14PS3/"
MEMBERS_URL_POSTFIX = "/members-list"

def print_html_parse_error():
    '''Prints generic error message when for BeautifulSoup
    parse problems'''
    print 'Something went wrong when trying to parse html'
    print 'The content has probably changed. Shit happens.'
    

def fix_args(args):
    '''Fix arguments provided by pyfibot, to be used
    with TeamStatsParser'''
    temp = args.strip()
    temp = temp.replace(' ', '+')
    return temp

def create_search_url(team_name):
    '''Append team_name to Ea Sport Nhl ps3 search_url'''
    temp = fix_args(team_name)
    search_url = 'http://www.easportsworld.com/en_US/clubs/nhl14/search' + \
        '?find[name]='
    search_url += temp
    search_url += '&find[abbreviation]=&find[size]=' + \
        '&find[acceptJoinRequest]=&find[public]=&find[lang]=' + \
        '&find[platform]=PS3&find[region]=&find[team_leagueId]=' + \
        '&find[teamId]=&find[active]=true&do-search=submit'
    return search_url

class TeamParser(object):
    '''Uses Beautifulsoup to parse team statistics from provided html'''
    def __init__(self):
        self._club_record = ""
        self._region = ""
        self._ranking = ""
        self._team_name = ""
        
    def team_name(self):
        return self._team_name
        
    def club_record(self):
        return self._club_record

    def region(self):
        return self._region
        
    def ranking(self):
        return self._ranking
                
    def parse(self, html=""):
        '''Do the parsing of html. After this method is finished
        individual data can be fetched e.g club_record()'''
        self._set_initial_values_to_empty()
        html = BeautifulSoup(html)
        try:
            team_header = html.find('div', {'class' : 'main-club-header'})
            self._team_name = team_header.h1.a.string
            stat_cells = self._find_stat_table_cells(html)
            self._club_record = stat_cells[0].span.string.replace(' ', '')
            self._region = stat_cells[1].string.replace("Region: ", "")
            self._ranking = \
                stat_cells[2].string.replace("Overall Ranking: ", "")
        except:
            print_html_parse_error()
            
    def _find_stat_table_cells(self, html):
        stats_table = html.find('table', 
            {'class' : 'plain full-width nowrap less-padding no-margin'})
        return stats_table.findAll('td')

        
    def _set_initial_values_to_empty(self):
        self._club_record = ""
        self._region = ""
        self._ranking = ""
        self._team_name = ""
    

class TeamUrlFinder(object):
    '''Finds team url from EA sports nhl 12 search results html'''
    def __init__(self, html=""):
        if html:
            self.html = BeautifulSoup(html)
        
    def get_url(self, number=1):
        '''Get the url, param number defines which url to get,
        in case there are more than one. Defaults always to first.'''
        try:
            containing_table = self.html.find('table', 
                {'class' : 'styled full-width'})
            links = containing_table.tbody.findAll('h4')
            postfix = links[number-1].a['href']
        except AttributeError:
            return ""
        except IndexError:
            return ""

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


def get_team_overview_data(team_name):
    content = None
    team = None
    try:
        team = Team.select().where(Team.name ** team_name).get()
    except DoesNotExist:
        pass
    if team:
        content = get_content(TEAM_URL_PREFIX + team.eaid + TEAM_URL_POSTFIX)
    else:
        team = save_new_team_to_db(team_name)
        if team:
            content = get_content(TEAM_URL_PREFIX + team.eaid + TEAM_URL_POSTFIX)
    return content if content else ""

def save_new_team_to_db(team_name):
    search_url = create_search_url(team_name)
    html = get_content(search_url)
    finder = TeamUrlFinder(html)
    team_url = finder.get_url()
    if team_url:
        ea_id = team_url.split('/')[-2]
        team = Team(name=team_name, platform=SYSTEM, eaid=ea_id)
        team.save()
        return team
    return None

def get_team_stats(team_html=""):
    '''Wrapper for TeamParser. Produces pyfibot friendly string
    for team stats'''
    parser = TeamParser()
    parser.parse(team_html)
    sentence = ""
    team_name = parser.team_name() 
    if team_name:
        sentence =  team_name + ' '
        sentence += parser.region() + ' '
        sentence += parser.club_record() + ' | '
        sentence += 'OR: ' + parser.ranking() + ' | '
    return sentence.strip()        

class PlayerParser(object):
    '''Parses player stats from given url'''
    def __init__(self):
        self.members = None
        self.tdcells = None
        self.team = None

    def parse(self, team, html=""):
        '''actual parsing, gets all the players in html
        as tr rows'''
        self.team = team
        html = BeautifulSoup(html)
        self.members = []
        try:
            member_table = html.find('table', 
                {'class' : 'styled full-width no-margin'}).tbody
            self.members = member_table.findAll('tr')
            for member in self.members:
                self.tdcells = member.findAll('td')
                player = self._create_player()
                player.save()
        except:
            print_html_parse_error()
            
    def _create_player(self):
        try:
            name = str(self.tdcells[1].div.a.string)
            player = Player.select().where(Player.name ** name).get()
            
        except DoesNotExist:
            player = Player()    
        
        try:
            player.name = str(self.tdcells[1].div.a.string)
            player.goals = str(self.tdcells[3].string)
            player.assists = str(self.tdcells[4].string)
            player.points = str(self.tdcells[5].string)
            player.plusminus = str(self.tdcells[6].string)
            player.penalties = str(self.tdcells[7].string)
            player.power_play_goals = str(self.tdcells[8].string)
            player.short_handed_goals = str(self.tdcells[9].string)
            player.hits = str(self.tdcells[10].string)
            player.blocked_shots = str(self.tdcells[11].string)
            player.shots = str(self.tdcells[12].string)
            player.team = self.team
            player.modified = datetime.now()
        except:
            print_html_parse_error()
            
        return player

def stats_of_player(player):
    '''Formats player stats for pyfibot'''
    stats = ""
    if (player):
        stats = \
            "%s G:%s A:%s +/-: %s PIM: %s Hits: %s BS: %s S: %s" \
            % (player.name, \
            player.goals, \
            player.assists, player.plusminus, player.penalties, \
            player.hits, player.blocked_shots, player.shots)
    return stats
