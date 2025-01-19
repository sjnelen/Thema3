"""
This module defines a SQLAlchemy model for storing and analyzing FASTA sequence entries.

The main class `FastaEntry` represents individual FASTA sequences with relevant metadata,
enabling storage and retrieval of sequence data and analysis results. It includes attributes like 
sequence length, GC content, nucleotide frequencies, and more.

Classes:
    FastaEntry: A SQLAlchemy model for storing and managing sequence data and results.
"""

__author__ = 'Sam Nelen'
__version__ = '2025.01.16'

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FastaEntry(db.Model):
    """
    Represents a FASTA file entry containing metadata and sequence information.

    The FastaEntry class models information for a single sequence entry in
    a FASTA file, including sequence data, associated description, file path,
    and calculated statistics such as nucleotide and codon frequencies, GC
    content, and protein sequence. It also records the upload date of the
    entry for tracking purposes.

    :ivar id: Unique identifier for the sequence entry (e.g., a sequence
        accession number or custom ID).
    :type id: str
    :ivar description: Description or header associated with the FASTA sequence,
        typically found after the '>' symbol in a FASTA format.
    :type description: str
    :ivar sequence: The nucleotide sequence in the FASTA entry.
    :type sequence: str
    :ivar filepath: Path to the file where the FASTA sequence is stored.
    :type filepath: str
    :ivar sequence_length: Length of the nucleotide sequence.
    :type sequence_length: int
    :ivar gc_content: The calculated GC content (percentage of G and C bases in
        the sequence).
    :type gc_content: float
    :ivar nuc_freq: Nucleotide frequency data stored as a serialized object.
        Typically, a dictionary where keys are nucleotides ('A', 'T', 'C', 'G')
        and values are their occurrence counts.
    :type nuc_freq: dict
    :ivar codon_freq: Codon frequency data stored as a serialized object.
        Typically, a dictionary where keys are codons (triplets of nucleotides)
        and values are their occurrence counts.
    :type codon_freq: dict
    :ivar protein_seq: Translated protein sequence corresponding to the FASTA
        nucleotide sequence, if applicable.
    :type protein_seq: str
    :ivar upload_date: Timestamp indicating when the FASTA entry was uploaded
        to the system.
    :type upload_date: datetime
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