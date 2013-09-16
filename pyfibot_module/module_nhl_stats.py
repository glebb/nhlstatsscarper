# -*- coding: utf-8 -*-

from eanhlstats.interface import *
import eanhlstats.settings

def command_ts(bot, user, channel, args):
    team = get_team(args)
    if not team:
        bot.say(channel, 'Team not found: ' + args)
        return
    data = get_team_stats(team)
    if not data:
        bot.say(channel, 'Error in fetching data for: ' + args)
        return
    
    bot.say(channel, stats_of_team(data))

def command_ps(bot, user, channel, args):
    if len(args.split('@')) == 2:
        team_string = args.split('@')[1]
        player_string = args.split('@')[0]
    else:
        team_string = eanhlstats.settings.DEFAULT_TEAM    
        player_string = args
    team = get_team(team_string)
    if not team:
        bot.say(channel, 'Team not found: ' + team_string)
        return
    player = get_player(player_string, team)
    if not player:
        bot.say(channel, 'Player ' + player_string + ' not found from team: ' + team.name)
    
    bot.say(channel, stats_of_player(player))
    
def command_switch(bot, user, channel, args):
    if eanhlstats.settings.SYSTEM == "PS3":
        eanhlstats.settings.SYSTEM = "XBX"
        bot.say(channel, 'Switched nhl stats to XBX')
    else:
        eanhlstats.settings.SYSTEM = "PS3"
        bot.say(channel, 'Switched nhl stats to PS3')
        
def command_top(bot, user, channel, args):
    team = get_team(args)
    if not team:
        bot.say(channel, 'Team not found: ' + args)
        return
    players = get_players(team)
    if not players:
        bot.say(channel, 'No player data found from team: ' + team.name)
    
    bot.say(channel, top_players(players, 5))
    