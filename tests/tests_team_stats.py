# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.realpath('../lib'))

import unittest

import fixtures
import fixtures_xbox
from eanhlstats.html import *

class TeamParserSpec(unittest.TestCase):
    def setUp(self):
        self.data = parse_team_overview_data(fixtures.murohoki_overview)
        self.data2 = parse_team_overview_data(fixtures_xbox.xbx_overview)

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
        self.data = parse_team_overview_data("")
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
            

class TeamUrlFinderSpec(unittest.TestCase):
    def setUp(self):
        pass
        
    def it_should_find_url_with_good_html(self):
        url = get_team_url(fixtures.murohoki_search)
        self.assertEqual(url, "http://www.easportsworld.com/en_US/clubs/NHL14PS3/26/overview")
        
    def it_should_not_find_url_with_bad_html(self):
        url = get_team_url("")
        self.assertEqual(url, None)
    
    def it_should_not_find_url_with_partly_good_html(self):
        url = get_team_url('<table class="styled full-width"></table>')
        self.assertEqual(url, None)
        
    def it_should_find_third_url_from_list_of_many_urls(self):
        url = get_team_url(fixtures.many_search_results, 3)
        self.assertEqual(url, "http://www.easportsworld.com/en_US/clubs/NHL14PS3/1272/overview")
    
    def it_should_return_empty_string_if_requested_url_index_too_big(self):
        url = get_team_url(fixtures.murohoki_search, 10)
        self.assertEqual(url, None)
            
        
    
    


