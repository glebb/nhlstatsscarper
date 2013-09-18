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
import eanhlstats.interface
from eanhlstats.model import *

test_db = SqliteDatabase(':memory:')
        
    
class InterfaceSpec(unittest.TestCase):
    def setUp(self):
        eanhlstats.html.team.get_content = MagicMock(return_value = "")
        self.team = Team(name="murohoki", platform="PS3", eaid="26")
        
    def tearDown(self):
        pass

    def it_should_print_stats_for_team(self):
        eanhlstats.interface.get_team_overview_html = MagicMock(return_value=fixtures_teamps3.murohoki_overview)   
        data = eanhlstats.interface.get_team_stats(self.team)
        self.assertEquals("murohoki Europe 24-24-7 | OR: 287", eanhlstats.interface.stats_of_team(data))

    def it_should_show_player_stats(self):
        with test_database(test_db, (Team, Player)):
            self.team.save()
            players = eanhlstats.html.players.parse_player_data(self.team, fixtures_members.murohoki_members)
            for player in players:
                player.save()
        
            player = eanhlstats.interface.get_player("qolazor", self.team)
            self.assertEquals("qolazor G:9 A:13 +/-:-23 PIM:72 Hits:62 BS:3 S:74", 
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
        self.assertEquals("Lost 0-3 against Deadly Phantoms HC | Lost 3-6 against Nordic Hockey Tigers | Won 4-0 against Kiitos EA", results)
        