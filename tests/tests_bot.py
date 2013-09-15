# -*- coding: utf-8 -*-

import sys, os
sys.path.insert(0, os.path.realpath('../lib'))

import unittest

import fixtures
from eanhlstats.html import *
from eanhlstats.db import search_player
import eanhlstats.settings
from eanhlstats.interface import *

class CreateSearchUrlSpec(unittest.TestCase):
    def it_creates_search_url_for_team_name(self):
        eanhlstats.settings.SYSTEM = "PS3"
        val = create_search_url("murohoki")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=murohoki&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')

    def it_creates_search_url_for_team_name_with_spaces(self):
        eanhlstats.settings.SYSTEM = "PS3"
        val = create_search_url("murohoki blaah")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=murohoki+blaah&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')
        
    def it_works_with_empty_param(self):
        eanhlstats.settings.SYSTEM = "PS3"
        val = create_search_url("")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')

    def it_creates_search_url_for_team_name_for_XBOX(self):
        eanhlstats.settings.SYSTEM = "XBX"
        val = create_search_url("murohoki")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=murohoki&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=360&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')


class BotFunctionsMemberStatsSpec(unittest.TestCase):
    def test_stats_of_player_shows_stats(self):
        team = Team(name="murohoki", platform="PS3", eaid="26")
        players = parse_player_data(team, fixtures.murohoki_members)
        player = next(player for player in players if player.name == 'qolazor')
        stats = stats_of_player(player)
        self.assertEqual(stats, "qolazor G:9 A:13 +/-: -23 PIM: 72 Hits: 62 BS: 3 S: 74")
    
