import unittest

import fixtures
from parse import *

class AcceptanceTests(unittest.TestCase):
    def it_should_print_stats_for_murohoki(self):
        args = "murohoki"
        number = get_order_from_args(args)
        html = get_html(args, number)    
        sentence = get_team_stats(html)
        self.assertTrue(sentence.find("murohoki Europe") != -1)

    def it_should_return_empty_for_unknonwn_name(self):
        args = "ldsjf2khskfsdf"
        number = get_order_from_args(args)
        html = get_html(args, number)    
        sentence = get_team_stats("")
        self.assertEqual("", sentence)

class TeamParserSpec(unittest.TestCase):
    def setUp(self):
        self.parser = TeamParser()
        self.parser.parse(fixtures.murohoki_overview)

    def it_should_find_team_name(self):
        team = self.parser.team_name()
        self.assertEqual("murohoki", team)

    def it_should_find_club_record(self):
        record = self.parser.club_record()
        self.assertEqual("62-14-5", record)

    def it_should_find_club_region(self):
        region = self.parser.region()
        self.assertEqual("Europe", region)

    def it_should_find_overall_ranking(self):
        ranking = self.parser.ranking()
        self.assertEqual("2", ranking)
        
    def it_should_return_empty_string_without_good_data(self):
        self.parser = TeamParser()
        self.parser.parse("")
        team = self.parser.team_name()
        self.assertEqual("", team)
        

class TeamUrlFinderSpec(unittest.TestCase):
    def setUp(self):
        pass
        
    def it_should_find_url_with_good_html(self):
        finder = TeamUrlFinder(fixtures.murohoki_search)
        url = finder.get_url()
        self.assertEqual(url, "http://www.easportsworld.com/en_US/clubs/501A0001/181/overview")
        
    def it_should_not_find_url_with_bad_html(self):
        finder = TeamUrlFinder("")
        url = finder.get_url()
        self.assertEqual(url, "")
    
    def it_should_not_find_url_with_partly_good_html(self):
        finder = TeamUrlFinder('<table class="styled full-width"></table>')
        url = finder.get_url()
        self.assertEqual(url, "")
        
    def it_should_find_third_url_from_list_of_many_urls(self):
        finder = TeamUrlFinder(fixtures.many_search_results)
        url = finder.get_url(3)
        self.assertEqual(url, "http://www.easportsworld.com/en_US/clubs/501A0001/325/overview")
    
    def it_should_return_empty_string_if_requested_url_index_too_big(self):
        finder = TeamUrlFinder(fixtures.murohoki_search)
        url = finder.get_url(10)
        self.assertEqual(url, "")
    
class BotFunctionsSpec(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_fix_args_returns_identical_string_in_case_of_single_word(self):
        args = fix_args("murohoki")
        self.assertEqual(args, "murohoki")
    
    def test_fix_args_should_convert_spaces_to_plus_signs(self):
        args = fix_args("hc kisaveikot")
        self.assertEqual(args, "hc+kisaveikot")
        
    def test_fix_args_should_remove_number_modifier_from_end(self):
        args = fix_args("hc |3")
        self.assertEqual(args, "hc")

    def test_fix_args_should_remove_number_modifier_from_end_without_space(self):
        args = fix_args("hc|3")
        self.assertEqual(args, "hc")

    def test_fix_args_should_detele_everything_after_specifier(self):
        args = fix_args("hc|blah")
        self.assertEqual(args, "hc")
        
    def test_get_order_from_args_returns_1_by_default(self):
        order = get_order_from_args("hc blaablaa")
        self.assertEqual(order, 1)
        
    def test_get_order_from_args_returns_specified_number(self):
        order = get_order_from_args("hc blaablaa |3")
        self.assertEqual(order, 3)
    
    def test_get_order_from_args_return_1_without_separator(self):
        order = get_order_from_args("hc blaablaa 10")
        self.assertEqual(order, 1)

    def test_get_order_from_args_returns_specified_big_number(self):
        order = get_order_from_args("hc blaablaa |10")
        self.assertEqual(order, 10)

    def test_get_order_from_args_works_with_space_after_separator(self):
        order = get_order_from_args("hc blaablaa | 2")
        self.assertEqual(order, 2)

    def test_get_order_from_args_returns_1_if_garbage_in_the_end(self):
        order = get_order_from_args("hc blaablaa |2 xcvcx")
        self.assertEqual(order, 1)

    def test_create_search_url_creates_search_url_for_team_name(self):
        val = create_search_url("murohoki")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl12/search?find[name]=murohoki&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')
        
    def test_create_search_url_works_with_empty_param(self):
        val = create_search_url("")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl12/search?find[name]=&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')

    def test_create_search_url_fixes_arguments(self):
        val = create_search_url("hc kisaveikot |3 zxcxz")
        self.assertEqual(val, 'http://www.easportsworld.com/en_US/clubs/nhl12/search?find[name]=hc+kisaveikot&find[abbreviation]=&find[size]=&find[acceptJoinRequest]=&find[public]=&find[lang]=&find[platform]=PS3&find[region]=&find[team_leagueId]=&find[teamId]=&find[active]=true&do-search=submit')
