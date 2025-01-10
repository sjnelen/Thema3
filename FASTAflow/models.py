"""Database module for the FASTAflow application

This module initializes the sqlite3 database for storing sequence variables
and some analysis results.

Attributes:
    db (SQLAlchemy): The SQLAlchemy database instance

Typical usage example:
    from FASTAflow.models import db, FastaEntry

    # Create a new entry
    entry = FastaEntry(
        header = '>sequence1',
        filepath = '/path/to/file.fasta'
    )
    db.session.add(entry)
    db.session.commit()

    # Query entries
    entries = FastaEntry.query.all()
"""

__author__ = 'Sam Nelen'
__version__ = '2024.08.22'

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FastaEntry(db.Model):
    """SQLAlchemy model for storing sequence variables and their analysis results.

    This model represents a single FASTA sequence entry and its metadata, including
    analysis results like GC content.

    Attributes:
        id (int): The primary key of the entry.
        description (str): The header line of the FASTA sequence, must be unique.
        filepath (str): The filepath of the FASTA sequence.
        sequence_length (int, optional): The length of the FASTA sequence.
        gc_content (int, optional): The GC content of the FASTA sequence.
        nuc_freq (dict, optional): The nucleotide frequencies of the FASTA sequence.
        upload_date (datetime): The date when the sequence was uploaded.

    Example:
        entry = FastaEntry(
            header = '>sequence1',
            filepath = '/path/to/file.fasta'
        )
        db.session.add(entry)
        db.session.commit()
        print(entry)
        'seq1 description'
    """

    id = db.Column(db.String, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    sequence = db.Column(db.Text, nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    sequence_length = db.Column(db.Integer)
    gc_content = db.Column(db.Float)
    nuc_freq = db.Column(db.PickleType)
    codon_freq = db.Column(db.PickleType)
    protein_seq = db.Column(db.Text)
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Sequence {self.id}>'