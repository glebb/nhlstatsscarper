# -*- coding: utf-8 -*-

import unittest

import fixtures
from nhl12statsparse.parse import *

class AcceptanceTestsTeamStats(unittest.TestCase):
    def it_should_print_stats_for_team(self):
        args = "murohoki"
        number = get_order_from_args(args)
        html = get_html(args, number)    
        sentence = get_team_stats(html)
        self.assertTrue(sentence.find("murohoki Europe") != -1)

    def it_should_return_empty_for_unknonwn_team_name(self):
        args = "ldsjf2khskfsdf"
        number = get_order_from_args(args)
        html = get_html(args, number)    
        sentence = get_team_stats("")
        self.assertEqual("", sentence)


class AcceptanceTestsPlayerStats(unittest.TestCase):
    def it_should_find_existing_player_stats(self):
        html = get_cached_content('http://www.easportsworld.com/en_US/clubs/partial/501A0001/181/members-list')
        self.assertTrue(html != None)
        parser = PlayerParser()
        parser.parse(html)
        player = parser.search("bodhi")
        self.assertTrue(player != None)
        self.assertEqual("bodhi-FIN", player.name)
