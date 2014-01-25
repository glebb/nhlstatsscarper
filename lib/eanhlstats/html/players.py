"""Player data parsing"""
# -*- coding: utf-8 -*-

import json

def get_player_ids(json_data):
    """Get Json and store member ids"""
    data = json.loads(json_data)
    temp = []
    data = data['raw'][0]
    for player in data.values():
        temp.append(player['blazeId'])
    return temp
        
def parse_player_data(json_data):
    """Return the actual list of dicts from JSON"""
    data = json.loads(json_data)
    if 'raw' in data:
        return data['raw']
    return None
    