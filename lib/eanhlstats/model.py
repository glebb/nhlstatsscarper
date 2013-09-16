from peewee import SqliteDatabase, Model, CharField, DateTimeField, DoesNotExist, IntegerField
import eanhlstats.settings

DB = SqliteDatabase('data.db', threadlocals=True)

class Team(Model):
    name = CharField()
    platform = CharField()
    eaid = CharField()
    
    class Meta:
        database = DB # this model uses the people database

class Player(Model):
    name = CharField()
    goals = IntegerField()
    assists = IntegerField()
    points = IntegerField()
    plusminus = IntegerField()
    penalties = IntegerField()
    power_play_goals = IntegerField()
    short_handed_goals = IntegerField()
    hits = IntegerField()
    blocked_shots = IntegerField()
    shots = IntegerField()
    team_eaid = CharField()
    platform = CharField()
    modified = DateTimeField()
    
    class Meta:
        database = DB # this model uses the people database
        
Team.create_table(True)
Player.create_table(True)

def get_player_from_db(player_name, team):
    '''Get a specific player from database, or return None.'''
    try:
        player = Player.select().where((Player.name ** player_name) & (Player.team_eaid ** team.eaid)
            & (Player.platform ** eanhlstats.settings.SYSTEM)).get()
        return player
    except DoesNotExist:
        return None

def get_players_from_db(team):
    '''Get all players from database for a specific team.'''
    return Player.select().where((Player.team_eaid ** team.eaid)
                & (Player.platform ** eanhlstats.settings.SYSTEM))

def get_team_from_db(team_name):
    try:
        team = Team.select().where((Team.name ** team_name) & (Team.platform ** eanhlstats.settings.SYSTEM)).get()    
        return team
    except DoesNotExist:
        return None