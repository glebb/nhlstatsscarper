# -*- coding: utf-8 -*-
from peewee import SqliteDatabase
from eanhlstats.model import *
from eanhlstats.interface import *
import eanhlstats.settings

Team.create_table(True)
Player.create_table(True)
eanhlstats.settings.REGION = 3

import logging
from twisted.internet import reactor

log = logging.getLogger("motionmachine")
result = None
trackchannel = None
trackbot = None


def init(bot):
    """Called when the bot is loaded and on rehash"""
    trackbot = None
    trackchannel = None
    result = None
    pp_motion_machine(60*2)

def pp_motion_machine(delay):
    """
    This will execute itself every <delay> seconds
    """
    global result
    global trackchannel
    global trackbot
    
    results = last_game("26")
    log.info(results)
    if results and (results != result) and trackchannel and trackbot:
        result = results
        trackbot.say(trackchannel, str(result))
        
    reactor.callLater(delay, pp_motion_machine, delay)
    
def command_trackresults(bot, user, channel, args):
    global trackbot
    global trackchannel
    trackbot = bot
    trackchannel = channel

def command_ts(bot, user, channel, args):
    if args.strip() != "":
        data = find_team_with_stats(args)
        if not data:
            bot.say(channel, 'Error in fetching data for: ' + str(args))
            return
        bot.say(channel, str(stats_of_team(data)))
    

def command_ps(bot, user, channel, args):
    bot.say(channel, 'Command disabled')
#     if args.strip() != "":
#         if len(args.split('@')) == 2:
#             team_string = args.split('@')[1]
#             player_string = args.split('@')[0]
#         else:
#             team_string = eanhlstats.settings.DEFAULT_TEAM    
#             player_string = args
#         team = get_team(team_string)
#         if team:
#             player = get_player(player_string, team)
#             if not player:
#                 bot.say(channel, 'Player ' + str(player_string) + ' not found from team: ' + str(team.name))
#                 return
#             bot.say(channel, str(stats_of_player(player)))
#         else:
#             bot.say(channel, 'Team not found: ' + str(team_string))
    
def command_switch(bot, user, channel, args):
    if eanhlstats.settings.SYSTEM == "PS3":
        eanhlstats.settings.SYSTEM = "XBX"
        bot.say(channel, 'Switched nhl stats to XBX')
    else:
        eanhlstats.settings.SYSTEM = "PS3"
        bot.say(channel, 'Switched nhl stats to PS3')
        
def command_top(bot, user, channel, args):
    bot.say(channel, 'Command disabled')
#     if args.strip() != "":
#         team = get_team(args)
#         if team:
#             players = get_players(team)
#             if not players:
#                 bot.say(channel, 'No player data found from team: ' + str(team.name))
#                 return
#             output = top_players(players, 5)
#             bot.say(channel, str(output))
#         else:
#             bot.say(channel, 'Team not found: ' + str(args))

def command_results(bot, user, channel, args):
   if args.strip() != "":
       team = find_team_with_stats(args)
       if team:
           results = last_games(5, eaid=team['eaid'])
           if not results:
               bot.say(channel, 'No results found for team ' + str(team.name) + ' for today.')
               return
           bot.say(channel, str(results))
       else:
           bot.say(channel, 'Team not found: ' + str(args))
    
def command_find(bot, user, channel, args):
    if args.strip() != "":
        teams = find_teams_by_abbreviation(args, 10)
        if teams:
            if len(teams) > 1:
                bot.say(channel, str(pretty_print_teams(teams, 10)))
                return
            elif len(teams) == 1:
                data = find_team_with_stats(teams[0].name)
                #data = get_team_stats(teams[0])
                if not data:
                    bot.say(channel, 'Error in fetching data for: ' + str(teams[0].name))
                    return
                bot.say(channel, str(stats_of_team(data)) + ' | ' + str(results_url(teams[0])))
                return
        bot.say(channel, 'Teams not found with: ' + str(args))
        