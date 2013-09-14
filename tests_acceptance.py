# -*- coding: utf-8 -*-

import unittest

from peewee import *

import fixtures
from nhlstatsparse.parse import *

class AcceptanceTestsTeamStats(unittest.TestCase):
    def it_should_print_stats_for_team(self):
        html = get_team_overview_data("murohoki")    
        sentence = get_team_stats(html)
        self.assertTrue(sentence.find("murohoki Europe") != -1)

    def it_should_return_empty_for_unknonwn_team_name(self):
        html = get_team_overview_data("ldsjf2khskfsdf")
        sentence = get_team_stats("")
        self.assertEqual("", sentence)
        
