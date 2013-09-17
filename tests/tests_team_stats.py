# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.realpath('../lib'))

import unittest
from mock import MagicMock
import fixtures
import fixtures_xbox
import eanhlstats.html.team
from eanhlstats.model import Team

class ParseTeamOverviewSpec(unittest.TestCase):
    def setUp(self):
        self.data = eanhlstats.html.team.parse_team_overview_data(fixtures.murohoki_overview)
        self.data2 = eanhlstats.html.team.parse_team_overview_data(fixtures_xbox.xbx_overview)

    def it_should_find_team_name(self):
        team = self.data['team_name']
        self.assertEqual("murohoki", team)

    def it_should_find_club_record(self):
        record = self.data['club_record']
        self.assertEqual("24-24-7", record)

    def it_should_find_club_region(self):
        region = self.data['region']
        self.assertEqual("Europe", region)

    def it_should_find_overall_ranking(self):
        ranking = self.data['ranking']
        self.assertEqual("287", ranking)
        
    def it_should_return_empty_string_without_good_data(self):
        self.data = eanhlstats.html.team.parse_team_overview_data("")
        self.assertEquals(None, self.data)

    def it_should_find_xbox_team_name(self):
        team = self.data2['team_name']
        self.assertEqual("ICE BANDITS", team)

    def it_should_find_xbox_club_record(self):
        record = self.data2['club_record']
        self.assertEqual("2-1-0", record)

    def it_should_find_xbox_club_region(self):
        region = self.data2['region']
        self.assertEqual("North America East", region)

    def it_should_find_xbox_overall_ranking(self):
        ranking = self.data2['ranking']
        self.assertEqual("11149", ranking)
            

class GetTeamUrlSpec(unittest.TestCase):
    def setUp(self):
        pass
        
    def it_should_find_url_with_good_html(self):
        url = eanhlstats.html.team.get_team_url(fixtures.murohoki_search)
        self.assertEqual(url, "http://www.easportsworld.com/en_US/clubs/NHL14PS3/26/overview")
        
    def it_should_not_find_url_with_bad_html(self):
        url = eanhlstats.html.team.get_team_url("")
        self.assertEqual(url, None)
    
    def it_should_not_find_url_with_partly_good_html(self):
        url = eanhlstats.html.team.get_team_url('<table class="styled full-width"></table>')
        self.assertEqual(url, None)
        
    def it_should_find_third_url_from_list_of_many_urls(self):
        url = eanhlstats.html.team.get_team_url(fixtures.many_search_results, 3)
        self.assertEqual(url, "http://www.easportsworld.com/en_US/clubs/NHL14PS3/1272/overview")
    
    def it_should_return_None_if_requested_url_index_too_big(self):
        url = eanhlstats.html.team.get_team_url(fixtures.murohoki_search, 10)
        self.assertEqual(url, None)
            
class CreateSearchUrlSpec(unittest.TestCase):
    def it_creates_search_url_for_team_name(self):
        eanhlstats.settings.SYSTEM = "PS3"
        val = eanhlstats.html.team.create_search_url("murohoki")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=murohoki&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')

    def it_creates_search_url_for_team_name_with_spaces(self):
        eanhlstats.settings.SYSTEM = "PS3"
        val = eanhlstats.html.team.create_search_url("murohoki blaah")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=murohoki+blaah&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')
        
    def it_works_with_empty_param(self):
        eanhlstats.settings.SYSTEM = "PS3"
        val = eanhlstats.html.team.create_search_url("")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')

    def it_creates_search_url_for_team_name_for_XBOX(self):
        eanhlstats.settings.SYSTEM = "XBX"
        val = eanhlstats.html.team.create_search_url("murohoki")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=murohoki&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=360&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')
    
class getTeamOverviewHtmlSpec(unittest.TestCase):
    def it_should_store_team_data_to_db(self):
        team_name = "this team does not exist already"
        fake_team = Team()
        fake_team.eaid = "0"
        eanhlstats.html.team.save_new_team_to_db = MagicMock(return_value=fake_team)
        eanhlstats.html.team.get_content = MagicMock(return_value=None)
        html = eanhlstats.html.team.get_team_overview_html(team_name)
        eanhlstats.html.team.save_new_team_to_db.assert_called_with(team_name)
            


