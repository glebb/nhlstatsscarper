# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.realpath('../lib'))

import unittest
from mock import MagicMock
from playhouse.test_utils import test_database
import fixtures_teamps3
import fixtures_teamxbox
import fixtures_results
import eanhlstats.html.team
from eanhlstats.model import Team
import eanhlstats.settings
from peewee import SqliteDatabase
from eanhlstats.model import *

data = eanhlstats.html.team.parse_team_overview_data(fixtures_teamps3.murohoki_standings)
data2 = eanhlstats.html.team.parse_team_overview_data(fixtures_teamxbox.xbx_standings)

test_db = SqliteDatabase(':memory:')

class ParseTeamOverviewSpec(unittest.TestCase):
    def setUp(self):
        pass

    def it_should_find_team_name(self):
        team = data['team_name']
        self.assertEqual("murohoki", team)

    def it_should_find_club_record(self):
        record = data['club_record']
        self.assertEqual("2-0-1", record)

    def it_should_find_club_region(self):
        region = data['region']
        self.assertEqual("Europe", region)

    def it_should_find_overall_ranking(self):
        ranking = data['ranking']
        self.assertEqual("284", ranking)
        
    def it_should_return_empty_string_without_good_data(self):
        data = eanhlstats.html.team.parse_team_overview_data("")
        self.assertEquals(None, data)

    def it_should_find_xbox_team_name(self):
        team = data2['team_name']
        print data2
        self.assertEqual("ice dogs", team)

    def it_should_find_xbox_club_record(self):
        record = data2['club_record']
        self.assertEqual("11-7-1", record)

    def it_should_find_xbox_club_region(self):
        region = data2['region']
        self.assertEqual("Europe", region)

    def it_should_find_xbox_overall_ranking(self):
        ranking = data2['ranking']
        self.assertEqual("5354", ranking)
            

class GetTeamUrlSpec(unittest.TestCase):
    def setUp(self):
        pass
        
    def it_should_find_url_with_good_html(self):
        data = eanhlstats.html.team.get_teams_from_search_page(fixtures_teamps3.murohoki_search)
        self.assertEqual(data[0]['url'], "http://www.easportsworld.com/en_US/clubs/NHL14PS3/26/standings")

    def it_should_find_team_name(self):
        data = eanhlstats.html.team.get_teams_from_search_page(fixtures_teamps3.murohoki_search)
        self.assertEqual(data[0]['name'], "murohoki")

    def it_should_not_find_url_with_bad_html(self):
        url = eanhlstats.html.team.get_teams_from_search_page("")
        self.assertEqual(url, None)
    
    def it_should_not_find_url_with_partly_good_html(self):
        url = eanhlstats.html.team.get_teams_from_search_page('<table class="styled full-width"></table>')
        self.assertEqual(url, None)
        
    def it_should_find_third_url_from_list_of_many_urls(self):
        data = eanhlstats.html.team.get_teams_from_search_page(fixtures_teamps3.many_search_results)
        self.assertEqual(data[2]['url'], "http://www.easportsworld.com/en_US/clubs/NHL14PS3/1272/standings")

    def it_should_find_team_name_from_list_of_many_urls(self):
        data = eanhlstats.html.team.get_teams_from_search_page(fixtures_teamps3.many_search_results)
        self.assertEqual(data[3]['name'], "ICEHOLES")
                
class CreateSearchUrlSpec(unittest.TestCase):
    def setUp(self):
        eanhlstats.settings.SYSTEM = "PS3"
        eanhlstats.settings.REGION = None

    def it_creates_search_url_for_team_name(self):
        val = eanhlstats.html.team.create_search_url("murohoki")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=murohoki&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')

    def it_creates_search_url_for_team_name_with_spaces(self):
        val = eanhlstats.html.team.create_search_url("murohoki blaah")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=murohoki+blaah&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')
        
    def it_works_with_empty_param(self):
        val = eanhlstats.html.team.create_search_url("")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')

    def it_creates_search_url_for_team_name_for_XBOX(self):
        eanhlstats.settings.SYSTEM = "XBX"
        val = eanhlstats.html.team.create_search_url("murohoki")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=murohoki&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=360&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')
        
    def it_creates_search_url_for_deafult_region(self):
        eanhlstats.settings.REGION = 3
        val = eanhlstats.html.team.create_search_url("")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=3&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')
        
    def it_creates_search_url_for_abbrevation_search(self):
        val = eanhlstats.html.team.create_search_url("mh", use_abbreviation=True)
        self.assertEquals(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=&find[abbreviation]=mh&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')
        
class GetTeamOverviewHtmlSpec(unittest.TestCase):
    def it_should_store_team_data_to_db(self):
        team_name = "this team does not exist already"
        fake_team = Team()
        fake_team.eaid = "0"
        eanhlstats.html.team.save_new_team_to_db = MagicMock(return_value=fake_team)
        eanhlstats.html.team.get_content = MagicMock(return_value=None)
        with test_database(test_db, (Team, Player)):
            html = eanhlstats.html.team.get_team_overview_html(team_name)
        eanhlstats.html.team.save_new_team_to_db.assert_called_with(team_name)
            
class GetResultsSpec(unittest.TestCase):
    def it_should_form_correct_url_for_results(self):
        eanhlstats.settings.SYSTEM = "PS3"
        url = eanhlstats.html.team.get_results_url("26")
        self.assertEquals('http://www.easportsworld.com/en_US/clubs/partial/NHL14PS3/26/match-results?type=all', url)

    def it_should_form_correct_url_for_results_for_XBX(self):
        eanhlstats.settings.SYSTEM = "XBX"
        url = eanhlstats.html.team.get_results_url("26")
        self.assertEquals('http://www.easportsworld.com/en_US/clubs/partial/NHL14XBX/26/match-results?type=all', url)
        
    def it_should_parse_first_match(self):
        data = eanhlstats.html.team.parse_results_data(fixtures_results.murohoki_results)
        self.assertEquals("Lost 0-3 against Deadly Phantoms HC", data[0])

    def it_should_parse_third_match(self):
        data = eanhlstats.html.team.parse_results_data(fixtures_results.murohoki_results)
        self.assertEquals("Won 4-0 against Kiitos EA", data[2])

    def it_should_handle_bad_html(self):
        data = eanhlstats.html.team.parse_results_data("")
        self.assertEquals(0, len(data))
    
class FindTeamsSpec(unittest.TestCase):
    def it_should_save_teams_to_db_when_finding_teams_by_abbreviation(self):
        eanhlstats.html.team.get_content = MagicMock(return_value = fixtures_teamps3.many_search_results)
        with test_database(test_db, (Team, Player)):
            teams = eanhlstats.html.team.find_teams("ice")
            self.assertEqual(10, len(teams))
            self.assertEquals(10, Team.select().count())

    def it_should_find_teams_by_abbreviation(self):
        with test_database(test_db, (Team, Player)):
            eanhlstats.html.team.get_content = MagicMock(return_value = fixtures_teamps3.many_search_results)
            results = eanhlstats.html.team.find_teams("ice")
            self.assertEqual(10, len(results))

    def it_should_note_save_teams_to_db_twice(self):
        eanhlstats.html.team.get_content = MagicMock(return_value = fixtures_teamps3.many_search_results)
        with test_database(test_db, (Team, Player)):
            teams = eanhlstats.html.team.find_teams("ice")
            teams = eanhlstats.html.team.find_teams("ice")
            self.assertEquals(10, Team.select().count())
    