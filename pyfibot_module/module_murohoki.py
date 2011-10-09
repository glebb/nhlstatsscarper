# -*- coding: utf-8 -*-

from parse import *
            
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
    murohoki_members_url = 'http://www.easportsworld.com/en_US/clubs/partial/501A0001/181/members-list'
    html = get_content(murohoki_members_url)
    parser = PlayerParser()
    parser.parse(html)
    player = self.parser.search(args)
    sentence = stats_for_player(player)
    if sentence:
        bot.say(channel, str(sentence))
    else:
        bot.say(channel, 'no results')
    return 
