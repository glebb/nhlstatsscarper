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
        eanhlstats.interface.get_team_overview_html = MagicMock(return_value=fixtures_teamps3.murohoki_standings)   
        data = eanhlstats.interface.get_team_stats(self.team)
        self.assertEquals("murohoki Europe GP: 153 | 81-58-14 | AGF: 2.37 | AGA: 2.33 | OR: 284", eanhlstats.interface.stats_of_team(data))

    def it_should_show_player_stats(self):
        with test_database(test_db, (Team, Player)):
            self.team.save()
            players = eanhlstats.html.players.parse_player_data(self.team, fixtures_members.murohoki_members)
            for player in players:
                player.save()
        
            player = eanhlstats.interface.get_player("qolazor", self.team)
            self.assertEquals("qolazor G:9 A:13 +/-:-23 PIM:72 Hits:62 BS:3 S:74 S%:12.2", 
                eanhlstats.interface.stats_of_player(player))

    def it_should_return_None_for_unknonwn_team_name(self):
        with test_database(test_db, (Team, Player)):
            sentence = eanhlstats.interface.get_team_stats(eanhlstats.interface.get_team("dsfdasfa23423qed"))
        self.assertEqual(None, sentence)
        
    def it_should_get_top_n_players_from_team(self):
        with test_database(test_db, (Team, Player)):
            self.team.save()
            players = eanhlstats.html.players.parse_player_data(self.team, fixtures_members.murohoki_members)
            for player in players:
                player.save()

            players = eanhlstats.interface.get_players(self.team)
            self.assertEquals("1.arielii (82), 2.HOLYDIVERS (63), 3.Mr_Fagstrom (48)", 
                eanhlstats.interface.top_players(players, 3))
        
    def it_should_get_last_n_games_from_team(self):
        eanhlstats.interface.get_content = MagicMock(return_value=fixtures_results.murohoki_results)
        results = eanhlstats.interface.last_games(self.team, 3)
        self.assertTrue(len(results) > 0)

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

    