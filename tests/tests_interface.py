# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.realpath('../src'))

import unittest
from mock import MagicMock
import fixtures_teamps3
import fixtures_json
import eashltoolkit.html.players
import eashltoolkit.html.team
import eashltoolkit.interface
    
class InterfaceSpec(unittest.TestCase):
    def setUp(self):
        eashltoolkit.html.team.get_content = MagicMock(return_value = "")
        
    def tearDown(self):
        pass

    def it_should_print_stats_for_team(self):
        eashltoolkit.interface.get_team_overview_json = MagicMock(return_value=fixtures_json.stats)
        data = eashltoolkit.interface.find_team_with_stats("murohoki")
        self.assertEquals("murohoki ID: 26 GP: 386 | 57.0% | 220-132-34 | AGF: 2.65 | AGA: 2.26 | Points: 1647", eashltoolkit.interface.stats_of_team(data))

    def it_should_print_player_stats(self):
        players = self._set_up_player_data()
        temp = eashltoolkit.interface.stats_of_player(players, "TEPPO WINNIPEG")
        self.assertEquals("D TEPPO WINNIPEG GP:176 G:38 A:85 +/-:68 PIM:214 Hits:615 BS:54 S:345 S%:11.0 GAA:0.00 SVP:0.000", temp)

    def it_should_return_None_for_unknonwn_team_name(self):
        eashltoolkit.interface.get_team_overview_json = MagicMock(return_value='[]')
        sentence = eashltoolkit.interface.find_team_with_stats("dsfdasfa23423qed")
        self.assertEqual(None, sentence)
        
    def it_should_get_top_players_sorted_by_key(self):
        players = self._set_up_player_data()
        temp = eashltoolkit.interface.sort_top_players(players, "skpoints", 2)
        self.assertEquals("1. ALIISA PRO (623), 2. SKIGE KAAKELI (558)", temp)

    def it_should_get_top_players_sorted_by_key_per_game(self):
        players = self._set_up_player_data()
        temp = eashltoolkit.interface.sort_top_players(players, "skgoals", 2, per_game=True)
        self.assertEquals("1. ALIISA PRO (0.98), 2. SKIGE KAAKELI (0.74)", temp)

    def it_should_return_None_with_invalid_key(self):
        players = self._set_up_player_data()
        temp = eashltoolkit.interface.sort_top_players(players, "blah", 2)
        self.assertEquals(None, temp)
        
    def it_should_get_last_n_games_from_team(self):
        eashltoolkit.interface.get_content = MagicMock(return_value=fixtures_json.results)
        results = eashltoolkit.interface.last_games(3, eaid="26")
        self.assertTrue(len(results) > 0)
        
    def it_should_print_last_game_for_team(self):
        eashltoolkit.interface.get_content = MagicMock(return_value=fixtures_json.results)
        results = eashltoolkit.interface.game_details(1, "26")
        self.assertEquals("Lost 2 - 3 against Backbreaker Project", results['summary'])
        self.assertEquals("LW arielii 1+0, D bodhi-FIN 0+0, D Noddactius 0+0, C Mr_Fagstrom 1+1, RW HOLYDIVERS 0+2", results['players'])

    def it_should_display_goalis_stats_for_game(self):
        eashltoolkit.interface.get_content = MagicMock(return_value=fixtures_json.results_including_6_players)
        results = eashltoolkit.interface.game_details(3, eaid="26")['players']
        self.assertEquals("D bodhi-FIN 0+1, D Noddactius 0+0, G Lionite 0+0 19/20 0.95%, RW JohnAbruzzzi_ 2+2, C HOLYDIVERS 0+3, LW arielii 3+0", results)


    def it_should_find_teams_by_abbreviation(self):
        eashltoolkit.html.team.get_content = MagicMock(return_value = fixtures_teamps3.many_search_results)
        teams = eashltoolkit.interface.find_teams_by_abbreviation("ice")
        teams = eashltoolkit.interface.pretty_print_teams(teams, 10)
        self.assertEquals("north american icemen, The IceBreakers, Ice Dogs, ICEHOLES, Icedroids, Natural Icers, IceAholics, Busch Ice, Snow Spiders, ICECAPS", teams)

    def it_should_cope_with_no_data(self):
        eashltoolkit.html.team.get_content = MagicMock(return_value = "<html></html>")
        teams = eashltoolkit.interface.find_teams_by_abbreviation("ice")
        self.assertEquals(None, teams)
        
    def _set_up_player_data(self):
        eashltoolkit.interface.get_content = MagicMock(return_value=fixtures_json.team_members)
        ids = eashltoolkit.interface.get_ids("26")
        eashltoolkit.interface.get_content = MagicMock(return_value=fixtures_json.members_stats)
        return eashltoolkit.interface.get_players("26", ids)
        