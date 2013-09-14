# -*- coding: utf-8 -*-

import unittest

import fixtures
from nhlstatsparse.parse import *

class TeamParserSpec(unittest.TestCase):
    def setUp(self):
        self.parser = TeamParser()
        self.parser.parse(fixtures.murohoki_overview)

    def it_should_find_team_name(self):
        team = self.parser.team_name()
        self.assertEqual("murohoki", team)

    def it_should_find_club_record(self):
        record = self.parser.club_record()
        self.assertEqual("24-24-7", record)

    def it_should_find_club_region(self):
        region = self.parser.region()
        self.assertEqual("Europe", region)

    def it_should_find_overall_ranking(self):
        ranking = self.parser.ranking()
        self.assertEqual("287", ranking)
        
    def it_should_return_empty_string_without_good_data(self):
        self.parser = TeamParser()
        self.parser.parse("")
        team = self.parser.team_name()
        self.assertEqual("", team)
            

class TeamUrlFinderSpec(unittest.TestCase):
    def setUp(self):
        pass
        
    def it_should_find_url_with_good_html(self):
        finder = TeamUrlFinder(fixtures.murohoki_search)
        url = finder.get_url()
        self.assertEqual(url, "http://www.easportsworld.com/en_US/clubs/NHL14PS3/26/overview")
        
    def it_should_not_find_url_with_bad_html(self):
        finder = TeamUrlFinder("")
        url = finder.get_url()
        self.assertEqual(url, "")
    
    def it_should_not_find_url_with_partly_good_html(self):
        finder = TeamUrlFinder('<table class="styled full-width"></table>')
        url = finder.get_url()
        self.assertEqual(url, "")
        
    def it_should_find_third_url_from_list_of_many_urls(self):
        finder = TeamUrlFinder(fixtures.many_search_results)
        url = finder.get_url(3)
        self.assertEqual(url, "http://www.easportsworld.com/en_US/clubs/NHL14PS3/1272/overview")
    
    def it_should_return_empty_string_if_requested_url_index_too_big(self):
        finder = TeamUrlFinder(fixtures.murohoki_search)
        url = finder.get_url(10)
        self.assertEqual(url, "")
        
        
    
    


