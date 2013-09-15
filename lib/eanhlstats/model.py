from peewee import SqliteDatabase, Model, CharField, DateTimeField, DoesNotExist
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
    goals = CharField()
    assists = CharField()
    points = CharField()
    plusminus = CharField()
    penalties = CharField()
    power_play_goals = CharField()
    short_handed_goals = CharField()
    hits = CharField()
    blocked_shots = CharField()
    shots = CharField()
    team_eaid = CharField()
    platform = CharField()
    modified = DateTimeField()
    
    class Meta:
        database = DB # this model uses the people database
        
Team.create_table(True)
Player.create_table(True)

def get_player_from_db(player_name, team):
    try:
        player = Player.select().where((Player.name ** player_name) & (Player.team_eaid ** team.eaid)
            & (Player.platform ** eanhlstats.settings.SYSTEM)).get()
        return player
    except DoesNotExist:
        return None

def get_team_from_db(team_name):
    try:
        team = Team.select().where((Team.name ** team_name) & (Team.platform ** eanhlstats.settings.SYSTEM)).get()    
        return team
    except DoesNotExist:
        return None

#def get_team_from_db_by_eaid(eaid):
#    try:
#        team = Team.select().where((Team.eaid ** eaid) & (Team.platform ** eanhlstats.settings.SYSTEM)).get()    
#        return team
#    except DoesNotExist:
#        return None
