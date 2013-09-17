# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.realpath('../lib'))

import unittest
from mock import MagicMock

import fixtures
from eanhlstats.html.players import *
from eanhlstats.model import *


class PlayerStatsSpec(unittest.TestCase):
    
    
    def setUp(self):
        self.team = Team(name="murohoki", platform="PS3", eaid="26")

    def it_should_find_stats_for_player(self):
        players = parse_player_data(self.team, fixtures.murohoki_members)
        self.player = next(player for player in players if player.name == 'qolazor')
        self.assertEqual("qolazor", self.player.name)
        self.assertEqual("9", self.player.goals)
        self.assertEqual("13", self.player.assists)
        self.assertEqual("22", self.player.points)
        self.assertEqual("-23", self.player.plusminus)
        self.assertEqual("72", self.player.penalties)
        self.assertEqual("3", self.player.power_play_goals)
        self.assertEqual("1", self.player.short_handed_goals)
        self.assertEqual("62", self.player.hits)
        self.assertEqual("3", self.player.blocked_shots)
        self.assertEqual("74", self.player.shots)
                
    def it_should_handle_bad_html(self):
        players = parse_player_data(self.team, "<html></html>")
        self.assertEqual(0, len(players))
        
    def it_should_sort_players_by_score(self):
        players = parse_player_data(self.team, fixtures.murohoki_members)
        