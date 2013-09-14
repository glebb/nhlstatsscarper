# -*- coding: utf-8 -*-

import unittest

import fixtures
from nhlstatsparse.parse import *

class FixArgsSpec(unittest.TestCase):
    def it_returns_identical_string_in_case_of_single_word(self):
        args = fix_args("murohoki")
        self.assertEqual(args, "murohoki")
    
    def it_should_convert_spaces_to_plus_signs(self):
        args = fix_args("hc kisaveikot")
        self.assertEqual(args, "hc+kisaveikot")
        
    def it_should_remove_number_modifier_from_end(self):
        args = fix_args("hc |3")
        self.assertEqual(args, "hc")

    def it_should_remove_number_modifier_from_end_without_space(self):
        args = fix_args("hc|3")
        self.assertEqual(args, "hc")

    def it_should_detele_everything_after_specifier(self):
        args = fix_args("hc|blah")
        self.assertEqual(args, "hc")

class GetOrderFromArgsSpec(unittest.TestCase):
    def it_returns_1_by_default(self):
        order = get_order_from_args("hc blaablaa")
        self.assertEqual(order, 1)
        
    def it_returns_specified_number(self):
        order = get_order_from_args("hc blaablaa |3")
        self.assertEqual(order, 3)
    
    def it__should_return_1_without_separator(self):
        order = get_order_from_args("hc blaablaa 10")
        self.assertEqual(order, 1)

    def it_returns_specified_big_number(self):
        order = get_order_from_args("hc blaablaa |10")
        self.assertEqual(order, 10)

    def it_works_with_space_after_separator(self):
        order = get_order_from_args("hc blaablaa | 2")
        self.assertEqual(order, 2)

    def it_returns_1_if_garbage_in_the_end(self):
        order = get_order_from_args("hc blaablaa |2 xcvcx")
        self.assertEqual(order, 1)

class CreateSearchUrlSpec(unittest.TestCase):
    def it_creates_search_url_for_team_name(self):
        val = create_search_url("murohoki")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=murohoki&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')
        
    def it_works_with_empty_param(self):
        val = create_search_url("")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')

    def it_fixes_arguments(self):
        val = create_search_url("hc kisaveikot |3 zxcxz")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl14/search?find[name]=hc+kisaveikot&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')

class BotFunctionsMemberStatsSpec(unittest.TestCase):
    def test_stats_of_player_shows_stats(self):
        parser = PlayerParser()
        parser.parse(fixtures.murohoki_members)
        player = parser.search("qolazor")
        stats = stats_of_player(player)
        self.assertEqual(stats, "qolazor G:9 A:13 +/-: -23 PIM: 72 Hits: 62 BS: 3 S: 74")
    
