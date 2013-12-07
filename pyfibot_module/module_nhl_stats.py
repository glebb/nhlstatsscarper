# -*- coding: utf-8 -*-
from eanhlstats.interface import *
import eanhlstats.settings

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
    
    results = last_game(eanhlstats.settings.DEFAULT_TEAM)
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
    if args.strip() != "":
        ids = get_ids(eanhlstats.settings.DEFAULT_TEAM)
        players = get_players(eanhlstats.settings.DEFAULT_TEAM, ids)
        temp = stats_of_player(players, args)
        if temp:
            bot.say(channel, temp)
        else:
            bot.say(channel, 'Error, spell name as it is in game')
    
# def command_switch(bot, user, channel, args):
#     if eanhlstats.settings.SYSTEM == "PS3":
#         eanhlstats.settings.SYSTEM = "XBX"
#         bot.say(channel, 'Switched nhl stats to XBX')
#     else:
#         eanhlstats.settings.SYSTEM = "PS3"
#         bot.say(channel, 'Switched nhl stats to PS3')
        
def command_top(bot, user, channel, args):
    if args.strip() != "":
        ids = eanhlstats.interface.get_ids(eanhlstats.settings.DEFAULT_TEAM)
        players = eanhlstats.interface.get_players(eanhlstats.settings.DEFAULT_TEAM, ids)
        temp = eanhlstats.interface.sort_top_players(players, args, 10)
        if temp:
            bot.say(channel, temp)
        else:
            bot.say(channel, 'Error, try "totalgp glso glsaves glga skpoints glgp glwins skshotpct skshots glgaa skgoals skhits skassists glsavepct skplusmin skppg skbs glsoperiods skshg skpim"')

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

def command_game(bot, user, channel, args):
   if not args or args.strip() != "":
       if not args.isdigit() or (int(args.strip()) <= 0 or int(args.strip()) >= 6):
           bot.say(channel, 'You should provide game number (1-5)')
           return
       results = game_details(int(args.strip()), eanhlstats.settings.DEFAULT_TEAM)
       if not results:
           bot.say(channel, 'Error')
           return
       bot.say(channel, results['summary'] + ' (' + results['when'] + ') | ' + results['players'])


    
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
        