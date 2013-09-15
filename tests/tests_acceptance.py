# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.realpath('../lib'))

import unittest

from peewee import *

import fixtures
from eanhlstats.html import *
from eanhlstats.interface import *

class InterfaceSpec(unittest.TestCase):
    def it_should_print_stats_for_team(self):
        team = get_team("murohoki")
        data = get_team_stats(team)
        self.assertEquals("murohoki", data['team_name'])
        self.assertEquals("Europe", data['region'])

    def it_should_print_stats_for_player(self):
        team = get_team("murohoki")
        player = get_player("qolazor", team)
        output = stats_of_player(player)
        self.assertTrue(output.startswith('qolazor G:'))

    def it_should_return_None_for_unknonwn_team_name(self):
        sentence = get_team_stats(get_team("dsfdasfa23423qed"))
        self.assertEqual(None, sentence)
        
