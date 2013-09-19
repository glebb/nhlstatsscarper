# -*- coding: utf-8 -*-
from peewee import SqliteDatabase
from eanhlstats.model import *
from eanhlstats.interface import *
import eanhlstats.settings

Team.create_table(True)
Player.create_table(True)
eanhlstats.settings.REGION = 3

def command_ts(bot, user, channel, args):
    team = get_team(args)
    if team:
        data = get_team_stats(team)
        if not data:
            bot.say(channel, 'Error in fetching data for: ' + args)
            return
        bot.say(channel, stats_of_team(data))
    else:
        bot.say(channel, 'Team not found: ' + args)
    

def command_ps(bot, user, channel, args):
    if len(args.split('@')) == 2:
        team_string = args.split('@')[1]
        player_string = args.split('@')[0]
    else:
        team_string = eanhlstats.settings.DEFAULT_TEAM    
        player_string = args
    team = get_team(team_string)
    if team:
        player = get_player(player_string, team)
        if not player:
            bot.say(channel, 'Player ' + player_string + ' not found from team: ' + team.name)
            return
        bot.say(channel, stats_of_player(player))
    else:
        bot.say(channel, 'Team not found: ' + team_string)
    
def command_switch(bot, user, channel, args):
    if eanhlstats.settings.SYSTEM == "PS3":
        eanhlstats.settings.SYSTEM = "XBX"
        bot.say(channel, 'Switched nhl stats to XBX')
    else:
        eanhlstats.settings.SYSTEM = "PS3"
        bot.say(channel, 'Switched nhl stats to PS3')
        
def command_top(bot, user, channel, args):
    team = get_team(args)
    if team:
        players = get_players(team)
        if not players:
            bot.say(channel, 'No player data found from team: ' + team.name)
            return
        bot.say(channel, top_players(players, 5))
    else:
        bot.say(channel, 'Team not found: ' + args)        

def command_results(bot, user, channel, args):
    team = get_team(args)
    if team:
        results = last_games(team, 3)
        if not results:
            bot.say(channel, 'No results found for team: ' + team.name)
            return
        bot.say(channel, results)
    else:
        bot.say(channel, 'Team not found: ' + args)        
    