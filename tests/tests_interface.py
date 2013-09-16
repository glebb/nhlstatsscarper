# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.realpath('../lib'))

import unittest
from peewee import *
import fixtures
import eanhlstats.html
import eanhlstats.interface
from eanhlstats.model import *

def fake_get_team_overview_html(team_name):
    return fixtures.murohoki_overview

def fake_refresh_player_data(team):
    team = Team(name="murohoki", platform="PS3", eaid="26")
    players = eanhlstats.html.parse_player_data(team, fixtures.murohoki_members)
    for player in players:
        player.save()
    
class InterfaceSpec(unittest.TestCase):
    def setUp(self):
        try:
            Player.delete()
            Team.delete()
        except:
            pass
        self.team = Team(name="murohoki", platform="PS3", eaid="26")
        self.team.save()
        eanhlstats.interface.get_team_overview_html = fake_get_team_overview_html   
        eanhlstats.interface._refresh_player_data = fake_refresh_player_data
        
    def tearDown(self):
        try:
            Player.delete()
            Team.delete()
        except:
            pass

    def it_should_print_stats_for_team(self):
        data = eanhlstats.interface.get_team_stats(self.team)
        self.assertEquals("murohoki Europe 24-24-7 | OR: 287", eanhlstats.interface.stats_of_team(data))

    def it_should_show_player_stats(self):
        player = eanhlstats.interface.get_player("qolazor", self.team)
        self.assertEquals("qolazor G:9 A:13 +/-:-23 PIM:72 Hits:62 BS:3 S:74", 
            eanhlstats.interface.stats_of_player(player))

    def it_should_return_None_for_unknonwn_team_name(self):
        sentence = eanhlstats.interface.get_team_stats(eanhlstats.interface.get_team("dsfdasfa23423qed"))
        self.assertEqual(None, sentence)
        
    def it_should_get_top_n_players_from_team(self):
        players = eanhlstats.html.parse_player_data(self.team, fixtures.murohoki_members)
        pass
        
        