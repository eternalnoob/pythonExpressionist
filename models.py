from database import db
from PCFG import from_json
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class Grammar(db.Model):
    __tablename__ = 'Grammars'
    id = db.Column(db.Integer, primary_key=True)
    grammar = db.Column(JSON)
    name = db.Column(db.String, unique=True)
    use_time = db.Column(db.DateTime)

    def __init__(self, grammar, name):
        self.grammar = grammar.to_json()
        self.name = name
        self.use_time = datetime.utcnow()

    def ret_obj(self):
        return from_json(self.grammar)

    def update(self, grammar):
        self.grammar = grammar.to_json()
        self.use_time = datetime.utcnow()

    def rename(self, name):
        self.name = name
        self.use_time = datetime.utcnow()
