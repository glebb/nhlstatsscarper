# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.realpath('../lib'))

import unittest
import fixtures_json
from eanhlstats.html.players import *
from eanhlstats.model import *
from playhouse.test_utils import test_database
test_db = SqliteDatabase(':memory:')


class PlayerStatsSpec(unittest.TestCase):
    
    
    def setUp(self):
        self.team = Team(name="murohoki", platform="PS3", eaid="26")

    def it_should_create_a_list_of_member_ids(self):
        players = get_player_ids(fixtures_json.team_members)
        self.assertEqual(9, len(players))
        self.assertTrue(172433139 in players)
        print players
        

    def it_should_find_stats_for_player(self):
        players = parse_player_data(fixtures_json.members_stats)
        
        self.player = next(player for player in players if player['playername'] == 'TEPPO WINNIPEG')
        self.assertEqual("TEPPO WINNIPEG", self.player['playername'])
        self.assertEqual("118", self.player['skpoints'])        
                
    def it_should_handle_bad_html(self):
        players = parse_player_data("[]")
        self.assertEqual(None, players)        