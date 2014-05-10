# -*- coding: utf-8 -*-
import logging

from eashltoolkit.interface import *
import eashltoolkit.settings
from twisted.internet import reactor


log = logging.getLogger("motionmachine")
result = None
trackchannel = None
trackbot = None


def init(bot):
    """Called when the bot is loaded and on rehash"""
    global trackbot
    global trackchannel
    global result
    trackbot = None
    trackchannel = None
    result = None


def pp_motion_machine(delay):
    """
    This will execute itself every <delay> seconds
    """
    global result
    global trackchannel
    global trackbot

    results = game_details(1, eashltoolkit.settings.DEFAULT_TEAM)
    if trackchannel and trackbot and results and (not result or (results['match_id'] != result['match_id'])):
        result = results
        temp = result['when'] + ' ' + result['home_team'] + ' ' + result['summary'] + ' (' + result['players'] + ')'
        trackbot.say(trackchannel, temp)

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
        command_game(bot, user, channel, "1 " + data['eaid'])


def command_ps(bot, user, channel, args):
    if args.strip() != "":
        ids = get_ids(eashltoolkit.settings.DEFAULT_TEAM)
        players = get_players(eashltoolkit.settings.DEFAULT_TEAM, ids)
        temp = stats_of_player(players, args)
        if temp:
            bot.say(user, temp)
        else:
            bot.say(user, 'Error, spell full name as it is in game')


#def command_switch(bot, user, channel, args):
#    if eashltoolkit.settings.SYSTEM == "PS3":
#        eashltoolkit.settings.SYSTEM = "XBOX"
#        bot.say(channel, 'Switched nhl stats to XBOX')
#    else:
#        eashltoolkit.settings.SYSTEM = "PS3"
#        bot.say(channel, 'Switched nhl stats to PS3')


def _split_team_id(args):
    if len(args.split(' ')) == 2:
        return args.split(' ')[0], args.split(' ')[1]
    else:
        return args, eashltoolkit.settings.DEFAULT_TEAM


def command_top(bot, user, channel, args):
    if args.strip() != "":
        args, team = _split_team_id(args)
        ids = eashltoolkit.interface.get_ids(team)
        players = eashltoolkit.interface.get_players(team, ids)
        temp = eashltoolkit.interface.sort_top_players(players, args)
        if temp:
            bot.say(user, temp)
        else:
            bot.say(user,
                    'Usage: .top skpoints <teamid>. Check alternatives for skpoints from https://raw.github.com/glebb/nhlstatsscarper/master/top_example.txt')


def command_top_pg(bot, user, channel, args):
    if args.strip() != "":
        args, team = _split_team_id(args)
        ids = eashltoolkit.interface.get_ids(team)
        players = eashltoolkit.interface.get_players(team, ids)
        temp = eashltoolkit.interface.sort_top_players(players, args, per_game=True)
        if temp:
            bot.say(user, temp)
        else:
            bot.say(user,
                    'Usage: .top_pg skpoints <teamid>. Check alternatives for skpoints from https://raw.github.com/glebb/nhlstatsscarper/master/top_example.txt')


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
        args, team = _split_team_id(args)
        if not args.isdigit() or (int(args.strip()) <= 0 or int(args.strip()) >= 6):
            bot.say(channel, 'Usage: .game 1 <teamid>. Game number goes up to 5.')
            return
        results = game_details(int(args.strip()), team)
        if not results:
            bot.say(channel, 'Error')
            return
        bot.say(channel, results['summary'] + ' (' + results['when'] + ') | ' + results['players'])


def command_find(bot, user, channel, args):
    if args.strip() != "":
        teams = find_teams_by_abbreviation(args)
        if teams:
            if len(teams) > 1:
                bot.say(channel, str(pretty_print_teams(teams, 10)))
                return
            elif len(teams) == 1:
                command_ts(bot, user, channel, teams[0]['name'])
                return
        bot.say(channel, 'Teams not found with: ' + str(args))


pp_motion_machine(60 * 2)
