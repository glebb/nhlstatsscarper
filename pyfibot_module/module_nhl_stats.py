# -*- coding: utf-8 -*-

from nhlstatsparse.parse import *
from datetime import datetime
from nhlstatsparse.db import search_player

def command_ts(bot, user, channel, args):
    html = get_team_overview_data(args)
    sentence = get_team_stats(html)
    if sentence:
        bot.say(channel, str(sentence))
    else:
        bot.say(channel, 'ei löydy tiimiä: ' + args)
    return

def command_ps(bot, user, channel, args):
    if len(args.split('@')) != 2:
        bot.say(channel, "Anna syöte muodossa pelaaja@joukkue")
        return
    try:
        team = Team.select().where(Team.name ** args.split('@')[1]).get()
    except:
        team = save_new_team_to_db(args.split('@')[1])
    
    if not team:
        bot.say(channel, "Tiimiä ei löydy: " + args.split('@')[1]) 
        return       
    
    player = None
    try:
        player = Player.select().where(Player.name ** args.split('@')[0]).get()
        delta = datetime.now() - player.modified
        if (delta.seconds / 60 >= 5):
            parser = PlayerParser()
            data = get_content(MEMBERS_URL_PREFIX + team.eaid + MEMBERS_URL_POSTFIX)
            parser.parse(team.name, data)
            player = search_player(args.split('@')[0])
    except:
        parser = PlayerParser()
        data = get_content(MEMBERS_URL_PREFIX + team.eaid + MEMBERS_URL_POSTFIX)
        parser.parse(team.name, data)
        player = search_player(args.split('@')[0])
                
    if not player:
        bot.say(channel, "Pelaajan tietoja ei löydy: " + args.split('@')[0])
        return
    bot.say(channel, stats_of_player(player))
    