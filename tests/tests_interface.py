# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.realpath('../lib'))

import unittest
from peewee import *
from mock import MagicMock
from playhouse.test_utils import test_database
import fixtures_teamps3
import fixtures_members
import fixtures_results
import fixtures_json
import eanhlstats.html.players
import eanhlstats.html.team
import eanhlstats.interface
from eanhlstats.model import *
import datetime

test_db = SqliteDatabase(':memory:')
        
    
class InterfaceSpec(unittest.TestCase):
    def setUp(self):
        eanhlstats.html.team.get_content = MagicMock(return_value = "")
        self.team = Team(name="murohoki", platform="PS3", eaid="26")
        
    def tearDown(self):
        pass

    def it_should_print_stats_for_team(self):
        eanhlstats.interface.get_team_overview_json = MagicMock(return_value=fixtures_json.stats)   
        data = eanhlstats.interface.find_team_with_stats(self.team.name)
        self.assertEquals("murohoki GP: 386 | 57.0% | 220-132-34 | AGF: 2.65 | AGA: 2.26 | Points: 1647", eanhlstats.interface.stats_of_team(data))

    def it_should_show_player_stats(self):
        eanhlstats.interface.get_content = MagicMock(return_value=fixtures_json.team_members)
        ids = eanhlstats.interface.get_ids("26")
        eanhlstats.interface.get_content = MagicMock(return_value=fixtures_json.members_stats)   
        players = eanhlstats.interface.get_players("26", ids)
        temp = eanhlstats.interface.stats_of_player(players, "TEPPO WINNIPEG")
        self.assertEquals("TEPPO WINNIPEG GP:171 G:36 A:82 +/-:66 PIM:212 Hits:595 BS:54 S:336 S%:10.7", temp)

    def it_should_return_None_for_unknonwn_team_name(self):
        eanhlstats.interface.get_team_overview_json = MagicMock(return_value='[]')   
        
        with test_database(test_db, (Team, Player)):
            sentence = eanhlstats.interface.find_team_with_stats("dsfdasfa23423qed")
        self.assertEqual(None, sentence)
        
    def it_should_get_top_players_sorted_by_key(self):
        eanhlstats.interface.get_content = MagicMock(return_value=fixtures_json.team_members)
        ids = eanhlstats.interface.get_ids("26")
        eanhlstats.interface.get_content = MagicMock(return_value=fixtures_json.members_stats)   
        players = eanhlstats.interface.get_players("26", ids)
        temp = eanhlstats.interface.sort_top_players(players, "skpoints", 2)
        self.assertEquals("1. ALIISA PRO (600), 2. SKIGE KAAKELI (543)", temp)

    def it_should_return_None_with_invalid_key(self):
        eanhlstats.interface.get_content = MagicMock(return_value=fixtures_json.team_members)
        ids = eanhlstats.interface.get_ids("26")
        eanhlstats.interface.get_content = MagicMock(return_value=fixtures_json.members_stats)   
        players = eanhlstats.interface.get_players("26", ids)
        temp = eanhlstats.interface.sort_top_players(players, "blah", 2)
        self.assertEquals(None, temp)

        
    def it_should_get_last_n_games_from_team(self):
        eanhlstats.interface.get_content = MagicMock(return_value=fixtures_json.results)
        results = eanhlstats.interface.last_games(3, self.team)
        self.assertTrue(len(results) > 0)
        
    def it_should_get_last_game_from_team(self):
        eanhlstats.interface.get_content = MagicMock(return_value=fixtures_json.results)
        results = eanhlstats.interface.last_game(self.team.eaid)
        self.assertEquals("Lost 2 - 3 against Backbreaker Project (arielii 1+0, bodhi-FIN 0+0, Noddactius 0+0, Mr_Fagstrom 1+1, HOLYDIVERS 0+2)", results)

    def it_should_find_teams_by_abbreviation(self):
        eanhlstats.html.team.get_content = MagicMock(return_value = fixtures_teamps3.many_search_results)
        with test_database(test_db, (Team, Player)):
            teams = eanhlstats.interface.find_teams_by_abbreviation("ice", 10)
            teams = eanhlstats.interface.pretty_print_teams(teams, 10)
            self.assertEquals("north american icemen, The IceBreakers, Ice Dogs, ICEHOLES, Icedroids, Natural Icers, IceAholics, Busch Ice, Snow Spiders, ICECAPS", teams)

    def it_should_cope_with_no_data(self):
        eanhlstats.html.team.get_content = MagicMock(return_value = "<html></html>")
        with test_database(test_db, (Team, Player)):
            teams = eanhlstats.interface.find_teams_by_abbreviation("ice", 10)
            self.assertEquals(None, teams)

    