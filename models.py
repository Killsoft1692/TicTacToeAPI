from datetime import datetime

from peewee import (
    Model,
    CharField,
    ForeignKeyField,
    TextField,
    DateTimeField
)

from settings import DB


class BaseModel(Model):
    class Meta:
        database = DB


class Player(BaseModel):
    username = CharField(unique=True)
    game_symbol = CharField(max_length=1)
    updated_at = DateTimeField(default=datetime.now)

    @classmethod
    def resolve_player_from_symbol(cls, given_symbol):
        return cls.select().order_by(cls.updated_at.desc()).where(
            cls.game_symbol == given_symbol
        ).get()


class Game(BaseModel):
    winner = ForeignKeyField(Player, backref='winner')
    looser = ForeignKeyField(Player, backref='looser')
    board = TextField()
    started_at = DateTimeField(default=datetime.now)
    stopped_at = DateTimeField()
