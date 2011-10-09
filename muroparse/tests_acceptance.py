# -*- coding: utf-8 -*-

import unittest

import fixtures
from parse import *

class AcceptanceTestsTeamStats(unittest.TestCase):
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


import os.path, time

def get_cached_content():
    if not os.path.exists("members.html"):
        return None
    now = time.time()
    FIVE_MINUTES = 60*5
    file_modified_time = os.path.getmtime('members.html')
    if (now - file_modified_time) > FIVE_MINUTES:
        return None    
    f = open('members.html', 'r')
    data = f.read()
    f.close()
    return data
    

class AcceptanceTestsPlayerStats(unittest.TestCase):
    def it_should_find_bodhi(self):
        html = get_cached_content()
        if not html:
            murohoki_members_url = 'http://www.easportsworld.com/en_US/clubs/partial/501A0001/181/members-list'
            html = get_content(murohoki_members_url)
            if html:
                f = open('members.html', 'w')
                f.write(html)
                f.close()
        self.assertTrue(html != None)
        parser = PlayerParser()
        parser.parse(html)
        player = parser.search("bodhi")
        self.assertTrue(player != None)
        self.assertEqual("bodhi-FIN", player.name)
