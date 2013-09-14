# -*- coding: utf-8 -*-

import unittest

import fixtures
from nhlstatsparse.parse import *
from nhlstatsparse.db import search_player

class FixArgsSpec(unittest.TestCase):
    def it_returns_identical_string_in_case_of_single_word(self):
        args = fix_args("murohoki")
        self.assertEqual(args, "murohoki")
    
    def it_should_convert_spaces_to_plus_signs(self):
        args = fix_args("hc kisaveikot")
        self.assertEqual(args, "hc+kisaveikot")
        
class CreateSearchUrlSpec(unittest.TestCase):
    def it_creates_search_url_for_team_name(self):
        val = create_search_url("murohoki")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=murohoki&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')
        
    def it_works_with_empty_param(self):
        val = create_search_url("")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')

class BotFunctionsMemberStatsSpec(unittest.TestCase):
    def test_stats_of_player_shows_stats(self):
        parser = PlayerParser()
        parser.parse("murohoki", fixtures.murohoki_members)
        player = search_player("qolazor")
        stats = stats_of_player(player)
        self.assertEqual(stats, "qolazor G:9 A:13 +/-: -23 PIM: 72 Hits: 62 BS: 3 S: 74")
    
