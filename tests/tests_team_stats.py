# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.realpath('../lib'))

import unittest
from mock import MagicMock
import fixtures_teamps3
import fixtures_json
import eanhlstats.html.team
import eanhlstats.settings

class TeamOverviewSpec(unittest.TestCase):
    def setUp(self):
        self.data = eanhlstats.html.team.find_team(fixtures_json.stats)

    def it_should_find_team_name(self):
        team = self.data['team_name']
        self.assertEqual("murohoki", team)

    def it_should_find_club_record(self):
        record = self.data['club_record']
        self.assertEqual("220-132-34", record)

    def it_should_find_overall_ranking(self):
        ranking = self.data['ranking']
        self.assertEqual("1647", ranking)
        

class TeamStandingsSpec(unittest.TestCase):
    def setUp(self):
        self.data = eanhlstats.html.team.find_team(fixtures_json.stats)

    def it_should_find_team_games_played(self):
        self.assertEqual("386", self.data['games_played'])
        
    def it_should_find_wins(self):
        self.assertEqual("220", self.data['wins'])

    def it_should_find_losses(self):
        self.assertEqual("132", self.data['losses'])        
        
    def it_should_find_average_goals_for(self):
        self.assertEqual("2.65", self.data['average_goals_for'])                
        
    def it_should_find_average_goals_against(self):
        self.assertEqual("2.26", self.data['average_goals_against'])                        

    def it_should_find_overtime_losses(self):
        self.assertEqual("34", self.data['overtime_losses'])            
                    
            
class GetResultsSpec(unittest.TestCase):
    def it_should_form_correct_url_for_match_results_ps3(self):
        eanhlstats.settings.SYSTEM = "PS3"
        url = eanhlstats.html.team.get_results_url("26")
        self.assertEquals('http://www.easports.com/iframe/nhl14proclubs/api/platforms/PS3/clubs/26/matches', url)

    def it_should_form_correct_url_for_match_results_xbox(self):
        eanhlstats.settings.SYSTEM = "XBOX"
        url = eanhlstats.html.team.get_results_url("26")
        self.assertEquals('http://www.easports.com/iframe/nhl14proclubs/api/platforms/XBOX/clubs/26/matches', url)
     
    def it_should_find_first_match_summary(self):
        self.data = eanhlstats.html.team.parse_results_data(fixtures_json.results, "26")
        self.assertEquals("Lost 2 - 3 against Backbreaker Project", self.data[0]['summary'])

    def it_should_find_first_match_time(self):
        self.data = eanhlstats.html.team.parse_results_data(fixtures_json.results, "26")
        self.assertEquals("2 minutes ago", self.data[0]['when'])

    def it_should_find_first_match_players(self):
        self.data = eanhlstats.html.team.parse_results_data(fixtures_json.results, "26")
        self.assertEquals("arielii 1+0, bodhi-FIN 0+0, Noddactius 0+0, Mr_Fagstrom 1+1, HOLYDIVERS 0+2", self.data[0]['players'])

    def it_should_find_third_match_summary(self):
        self.data = eanhlstats.html.team.parse_results_data(fixtures_json.results, "26")
        self.assertEquals("Won 2 - 1 against MGM Hockey", self.data[2]['summary'])

    def it_should_find_fourth_match_summary(self):
        self.data = eanhlstats.html.team.parse_results_data(fixtures_json.results, "26")
        self.assertEquals("Won 9 - 1 against Inarin PalloSeura", self.data[3]['summary'])

    def it_should_handle_bad_data(self):
        self.data = eanhlstats.html.team.parse_results_data('[]', "26")
        self.assertEquals(0, len(self.data))
    
class FindTeamsSpec(unittest.TestCase):
    def it_should_find_teams_by_abbreviation(self):
        eanhlstats.html.team.get_content = MagicMock(return_value = fixtures_teamps3.many_search_results)
        results = eanhlstats.html.team.find_teams("ice")
        self.assertEqual(10, len(results))   
        
    def it_shoould_form_correct_search_url_for_xbox(self):
        eanhlstats.settings.SYSTEM = "XBOX"
        url = eanhlstats.html.team.create_search_url("ice")
        self.assertEquals("http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=&find[abbreviation]=ice&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=360&find[region]=3&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit", url)

    def it_shoould_form_correct_search_url_for_ps3(self):
        eanhlstats.settings.SYSTEM = "PS3"
        url = eanhlstats.html.team.create_search_url("ice")
        self.assertEquals("http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=&find[abbreviation]=ice&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=3&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit", url)
                         