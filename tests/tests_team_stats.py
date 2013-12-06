# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.realpath('../lib'))

import datetime
import unittest
from mock import MagicMock
from playhouse.test_utils import test_database
import fixtures_teamps3
import fixtures_teamxbox
import fixtures_results
import fixtures_json
import eanhlstats.html.team
from eanhlstats.model import Team
import eanhlstats.settings
from peewee import SqliteDatabase
from eanhlstats.model import *

data = eanhlstats.html.team.find_team(fixtures_json.stats)

test_db = SqliteDatabase(':memory:')

class TeamOverviewSpec(unittest.TestCase):
    def setUp(self):
        pass

    def it_should_find_team_name(self):
        team = data['team_name']
        self.assertEqual("murohoki", team)

    def it_should_find_club_record(self):
        record = data['club_record']
        self.assertEqual("220-132-34", record)

    def it_should_find_overall_ranking(self):
        ranking = data['ranking']
        self.assertEqual("1647", ranking)
        
    def it_should_return_empty_string_without_good_data(self):
        data = eanhlstats.html.team.parse_team_standings_data("[]")
        self.assertEquals(None, data)

class TeamStandingsSpec(unittest.TestCase):
    def it_should_find_team_games_played(self):
        self.assertEqual("386", data['games_played'])
        
    def it_should_find_wins(self):
        self.assertEqual("220", data['wins'])

    def it_should_find_losses(self):
        self.assertEqual("132", data['losses'])        
        
    def it_should_find_average_goals_for(self):
        self.assertEqual("2.65", data['average_goals_for'])                
        
    def it_should_find_average_goals_against(self):
        self.assertEqual("2.26", data['average_goals_against'])                        

    def it_should_find_overtime_losses(self):
        self.assertEqual("34", data['overtime_losses'])            
        
class TeamDatabaseSpec(unittest.TestCase):        
    def it_should_save_teams_to_db_when_finding_teams_by_abbreviation(self):
        eanhlstats.html.team.get_content = MagicMock(return_value = fixtures_teamps3.many_search_results)
        with test_database(test_db, (Team, Player)):
            teams = eanhlstats.html.team.find_teams("ice")
            self.assertEqual(10, len(teams))
            self.assertEquals(10, Team.select().count())
            
            
class GetResultsSpec(unittest.TestCase):
    def it_should_form_correct_url_for_results(self):
        eanhlstats.settings.SYSTEM = "PS3"
        d = datetime.datetime(2013,10,10, 22, 0)
        url = eanhlstats.html.team.get_results_url("26")
        self.assertEquals('http://www.easports.com/iframe/nhl14proclubs/api/platforms/PS3/clubs/26/matches', url)

    def it_should_form_correct_url_for_results_for_XBOX(self):
        eanhlstats.settings.SYSTEM = "XBOX"
        d = datetime.datetime(2013,10,10, 22, 0)
        url = eanhlstats.html.team.get_results_url("26")
        self.assertEquals('http://www.easports.com/iframe/nhl14proclubs/api/platforms/XBOX/clubs/26/matches', url)
     
    def it_should_find_first_match(self):
        data = eanhlstats.html.team.parse_results_data(fixtures_json.results, "26")
        self.assertEquals("Lost 0 - 2 against Shamefull Knights (2 days ago)", data[0])

    def it_should_find_third_match(self):
        data = eanhlstats.html.team.parse_results_data(fixtures_json.results, "26")
        self.assertEquals("Lost 4 - 5 against Mister Sisters (2 days ago)", data[2])

    def it_should_find_fourth_match(self):
        data = eanhlstats.html.team.parse_results_data(fixtures_json.results, "26")
        self.assertEquals("Won 3 - 0 against Evoluution Umpikujat vol2 (3 days ago)", data[3])

    def it_should_handle_bad_data(self):
        data = eanhlstats.html.team.parse_results_data('[]', "26")
        self.assertEquals(0, len(data))
    
class FindTeamsSpec(unittest.TestCase):
    def it_should_find_teams_by_abbreviation(self):
        with test_database(test_db, (Team, Player)):
            eanhlstats.html.team.get_content = MagicMock(return_value = fixtures_teamps3.many_search_results)
            results = eanhlstats.html.team.find_teams("ice")
            self.assertEqual(10, len(results))                    