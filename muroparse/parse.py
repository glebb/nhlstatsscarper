from BeautifulSoup import BeautifulSoup
import urllib2

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

    def region(self):
        return self._region
        
    def ranking(self):
        return self._ranking
        
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
        except:
            print 'Something went wrong when trying to parse team results'
            print 'The html has probably changed. Shit happens.'

    def _find_stat_table_cells(self, html):
        stats_table = html.find('table', {'class' : 'plain full-width nowrap less-padding no-margin'})
        return stats_table.findAll('td')

        
    def _set_initial_values_to_empty(self):
        self._club_record = ""
        self._region = ""
        self._ranking = ""
        self._team_name = ""
    

class TeamUrlFinder(object):
    def __init__(self, html=""):
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
            h = urllib2.urlopen(url)
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
        sentence += 'OR: ' + parser.ranking()
    return sentence.strip()



