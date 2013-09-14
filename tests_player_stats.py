# -*- coding: utf-8 -*-

import unittest

import fixtures
from nhlstatsparse.parse import *
from nhlstatsparse.db import search_player

class PlayerStatsSpec(unittest.TestCase):
    def setUp(self):
        self.parser = PlayerParser()
        self.parser.parse("murohoki", fixtures.murohoki_members)
        self.player = search_player("qolazor")

    def it_should_find_stats_for_player(self):
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
        
    def it_should_handle_unknown_player(self):
        self.player = search_player("xysfsda")
        self.assertEqual(None, self.player)
        
    def it_should_handle_bad_html(self):
        self.parser.parse("xxx")
        self.player = search_player("bodhi")
        self.assertEqual(None, self.player)
    
    def it_should_handle_umlauts(self):
        self.player = search_player("äöääöäcx.,.123")
        self.assertEqual(None, self.player)