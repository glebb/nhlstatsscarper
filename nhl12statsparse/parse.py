# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib2
import os.path, time


def print_html_parse_error():
    print 'Something went wrong when trying to parse html'
    print 'The content has probably changed. Shit happens.'
    

def fix_args(args):
    splitted = args.split('|')
    if len(splitted) > 1:
        splitted.pop()
        temp = "".join(splitted)
        temp = temp.strip()
    else:
        temp = args
    temp = temp.replace(' ', '+')

    return temp

def get_order_from_args(args):    
    try:
        index = args.find('|')
        number = int(args[index+1:])
        return number
    except ValueError:
        return 1

def create_search_url(team_name):
    fixed_name = fix_args(team_name)
    search_url = 'http://www.easportsworld.com/en_US/clubs/nhl12/search?find[name]='
    search_url += fixed_name
    search_url += '&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit'
    return search_url

class TeamParser(object):
    def __init__(self):
        self._set_initial_values_to_empty()
        
    def team_name(self):
        return self._team_name
        
    def club_record(self):
        return self._club_record

    def club_record_overall(self):
        return self._club_record_overall

    def games_played(self):
        return self._games_played

    def region(self):
        return self._region
        
    def ranking(self):
        return self._ranking
        
    def last_game(self, html=""):
        result = ""
        if html:
            soup = BeautifulSoup(html)
            try:
                teams = soup.findAll('a', {'class' : 'secondary'})
                goals = soup.findAll('td', {'class': 'score strong'})
                result = teams[0].string + '-' + teams[1].string + ' ' + \
                    goals[0].string + '-' + goals[1].string
            except:
                print_html_parse_error()
        return result
        
    def parse(self, html=""):
        self._set_initial_values_to_empty()
        html = BeautifulSoup(html)
        try:
            team_header = html.find('div', {'class' : 'main-club-header'})
            self._team_name = team_header.h1.a.string
            stat_cells = self._find_stat_table_cells(html)
            self._club_record = stat_cells[1].span.string.replace(' ', '')
            self._region = stat_cells[2].string.replace("Region: ", "")
            self._ranking = stat_cells[4].string.replace("Overall Ranking: ", "")
            club_stats_cells = html.find('tr', {'class' : 'even strong black'}).findAll('td')
            self._club_record_overall = club_stats_cells[3].string + '-' + \
                club_stats_cells[4].string + '-' + club_stats_cells[5].string
            self._games_played = club_stats_cells[2].string
        except:
            print_html_parse_error()
            
    def _find_stat_table_cells(self, html):
        stats_table = html.find('table', {'class' : 'plain full-width nowrap less-padding no-margin'})
        return stats_table.findAll('td')

        
    def _set_initial_values_to_empty(self):
        self._club_record = ""
        self._club_record_overall = ""
        self._region = ""
        self._ranking = ""
        self._team_name = ""
        self._games_played = ""
    

class TeamUrlFinder(object):
    def __init__(self, html=""):
        if html:
            self.html = BeautifulSoup(html)
        
    def get_url(self, number=1):
        try:
            containing_table = self.html.find('table', {'class' : 'styled full-width'})
            links = containing_table.tbody.findAll('h4')
            postfix = links[number-1].a['href']
        except AttributeError:
            return ""
        except IndexError:
            return ""

        prefix = 'http://www.easportsworld.com'
        return prefix + postfix


def get_content(url):
    '''untested copy/paste code'''
    content = None
    if url:
        try:
            h = urllib2.urlopen(url, timeout=60)
            content = h.read()
            h.close()
        except IOError, e:
            print 'We failed to open "%s".' % url
            if hasattr(e, 'code'):
                print 'We failed with error code - %s.' % e.code
            elif hasattr(e, 'reason'):
                print "The error object has the following 'reason' attribute :"
                print e.reason
                print "This usually means the server doesn't exist,",
                print "is down, or we don't have an internet connection."
    return content


def get_html(args, number):
    search_url = create_search_url(args)
    html = get_content(search_url)
    finder = TeamUrlFinder(html)
    team_url = finder.get_url(number)
    content = get_content(team_url)
    return content if content else ""

def get_team_stats(team_html=""):
    parser = TeamParser()
    parser.parse(team_html)
    sentence = ""
    team_name = parser.team_name() 
    if team_name:
        sentence =  team_name + ' '
        sentence += parser.region() + ' '
        sentence += parser.club_record() + ' | '
        sentence += 'OR: ' + parser.ranking() + ' | '
        sentence += parser.club_record_overall()
    return sentence.strip()

class Player(object):
    def __init__(self):
        self.name = ""
        self.ranking = ""
        self.games_played = ""
        self.goals = ""
        self.assists = ""
        self.points = ""
        self.plusminus = ""
        self.penalties = ""
        self.power_play_goals = ""
        self.short_handed_goals = ""
        self.hits = ""
        self.blocked_shots = ""
        self.shots = ""
        

class PlayerParser(object):
    def __init__(self):
        self.members = None

    def parse(self, html=""):
        html = BeautifulSoup(html)
        self.members = []
        try:
            member_table = html.find('table', {'class' : 'styled full-width no-margin'}).tbody
            self.members = member_table.findAll('tr')
        except:
            print_html_parse_error()
            
    def search(self, search_name):
        player = None
        for member in self.members:
            tdcells = member.findAll('td')
            name = str(tdcells[1].div.a.string)
            if name.lower().find(search_name.lower()) != -1:
                player = self._create_player(tdcells)
                break
        return player

    def _create_player(self, tdcells):
        player = Player()
        try:
            player.name = str(tdcells[1].div.a.string)
            player.ranking = str(tdcells[3].string)
            player.games_played = str(tdcells[4].string)
            player.goals = str(tdcells[5].string)
            player.assists = str(tdcells[6].string)
            player.points = str(tdcells[7].string)
            player.plusminus = str(tdcells[8].string)
            player.penalties = str(tdcells[9].string)
            player.power_play_goals = str(tdcells[10].string)
            player.short_handed_goals = str(tdcells[11].string)
            player.hits = str(tdcells[12].string)
            player.blocked_shots = str(tdcells[13].string)
            player.shots = str(tdcells[14].string)
        except:
            print_html_parse_error()
            
        return player

def stats_of_player(player):
    stats = ""
    if (player):
        stats = "%s Pts:%s GP:%s G:%s A:%s +/-: %s PIM: %s Hits: %s BS: %s S: %s" %(player.name, \
        player.points, player.games_played, player.goals, player.assists, player.plusminus, player.penalties, \
        player.hits, player.blocked_shots, player.shots)
    return stats
    
def get_cached_content(team_members_url):
    if not os.path.exists("members.html"):
		return get_and_cache_team_members_html(team_members_url)    
    now = time.time()
    FIVE_MINUTES = 60*5
    file_modified_time = os.path.getmtime('members.html')
    
    if (now - file_modified_time) > FIVE_MINUTES:
		return get_and_cache_team_members_html(team_members_url)
        
    f = open('members.html', 'r')
    data = f.read()
    f.close()
    return data
    
def get_and_cache_team_members_html(url):
	html = get_content(url)
	if html:
		f = open('members.html', 'w')
		f.write(html)
		f.close()
	return html


    