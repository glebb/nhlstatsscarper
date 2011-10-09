# -*- coding: utf-8 -*-

TEAM_MEMBERS_URL = 'http://www.easportsworld.com/en_US/clubs/partial/501A0001/181/members-list'

from nhl12statsparse.parse import *
            
def command_tn(bot, user, channel, args):
    number = get_order_from_args(args)
    html = get_html(args, number)    
    sentence = get_team_stats(html)
    if sentence:
        bot.say(channel, str(sentence))
    else:
        bot.say(channel, 'no results')
    return 

def command_ps(bot, user, channel, args):
    html = get_cached_content(TEAM_MEMBERS_URL)
    parser = PlayerParser()
    parser.parse(html)
    player = self.parser.search(args)
    sentence = stats_for_player(player)
    if sentence:
        bot.say(channel, str(sentence))
    else:
        bot.say(channel, 'no results')
    return 
