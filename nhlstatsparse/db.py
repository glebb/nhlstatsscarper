from peewee import SqliteDatabase, Model, CharField, DateTimeField, DoesNotExist

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
    team = CharField()
    modified = DateTimeField()
    
    class Meta:
        database = DB # this model uses the people database
        
Team.create_table(True)
Player.create_table(True)

def search_player(name):
    try:
        player = Player.select().where(Player.name ** name).get()
        return player
    except DoesNotExist:
        return None
