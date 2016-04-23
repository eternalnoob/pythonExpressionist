from __init__ import db
from PCFG import from_json
from sqlalchemy.dialects.postgresql import JSON

class Grammar(db.Model):
    __tablename__ = 'Grammars'
    id = db.Column(db.Integer, primary_key=True)
    grammar = db.Column(JSON)

    def __init__(self, grammar):
        self.grammar = grammar

    def ret_obj(self):
        return from_json(self.grammar)

    def update(self, grammar):
        self.grammar = grammar