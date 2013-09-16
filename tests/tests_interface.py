# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.realpath('../lib'))

import unittest
from mock import MagicMock
from peewee import *
import eanhlstats.model
import fixtures
from eanhlstats.html import *
import eanhlstats.interface 

class InterfaceSpec(unittest.TestCase):
    def it_should_print_stats_for_team(self):
        team = eanhlstats.interface.get_team("murohoki")
        data = eanhlstats.interface.get_team_stats(team)
        self.assertEquals("murohoki", data['team_name'])
        self.assertEquals("Europe", data['region'])

    def it_should_show_player_stats(self):
        team = eanhlstats.model.Team(name="murohoki", platform="PS3", eaid="26")
        players = parse_player_data(team, fixtures.murohoki_members)
        player = next(player for player in players if player.name == 'qolazor')
        stats = eanhlstats.interface.stats_of_player(player)
        self.assertEqual(stats, "qolazor G:9 A:13 +/-: -23 PIM: 72 Hits: 62 BS: 3 S: 74")

    def it_should_return_None_for_unknonwn_team_name(self):
        sentence = eanhlstats.interface.get_team_stats(eanhlstats.interface.get_team("dsfdasfa23423qed"))
        self.assertEqual(None, sentence)
        