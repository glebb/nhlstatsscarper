# -*- coding: utf-8 -*-

from nhlstatsparse.parse import *
            
def command_tn(bot, user, channel, args):
    number = get_order_from_args(args)
    html = get_html(args, number)    
    sentence = get_team_stats(html)
    if sentence:
        bot.say(channel, str(sentence))
    else:
        bot.say(channel, 'no results')
    return 