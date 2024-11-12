import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FastaEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(500), nullable=False, unique=True)
    filepath = db.Column(db.String(500), nullable=False)
    sequence_length = db.Column(db.Integer)
    gc_content = db.Column(db.Float)
    nuc_freq = db.Column(db.PickleType)
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'FastaEntry(header="{self.header}", sequence_length="{self.sequence_length}")'