'''Player data parsing'''
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from datetime import datetime
import eanhlstats.settings
from eanhlstats.html.common import get_content
import json

def get_player_ids(json_data):
    data = json.loads(json_data)
    temp = []
    data = data['raw'][0]
    for player in data.values():
        temp.append(player['blazeId'])
    return temp
        
def parse_player_data(json_data):
    data = json.loads(json_data)
    if 'raw' in data:
        return data['raw']
    return None
    