"""
This module provides functionality for reading and storing sequences from FASTA files into a database.

It uses Biopython for parsing FASTA files and SQLAlchemy for interacting with the database.
Sequences that are already in the database are not duplicated, while new sequences are added.
Error handling is implemented for file I/O and database operations.
"""

__author__ = 'Sam Nelen'
__version__ = '2025.01.16'

from Bio import SeqIO
import logging
from sqlalchemy.exc import SQLAlchemyError

from FASTAflow.models import db, FastaEntry


def store_fasta_in_db(filepath):
    """Reads and parses the FASTA file.
    
    Args:
      filepath: Path to the FASTA file.
    
    Returns:
      list: List of Bio.SeqRecord objects representing the sequences in the FASTA file.
    
    Raises:
      IOError: If the FASTA file cannot be opened or read.
    """
    entries = []
    
    try:
        with open(filepath, 'r') as file_handle:
            for record in SeqIO.parse(file_handle, 'fasta'):
                # Check if sequence id already is in the database
                entry = db.session.query(FastaEntry).filter_by(id=record.id).first()

                if entry:
                    logging.info(f'Sequence with ID {record.id} already exists in the database, using existing entry')
                else:
                    # Create new entry if it doesn't exist
                    entry = FastaEntry(
                        id=record.id,
                        description=record.description,
                        sequence=str(record.seq),
                        filepath=filepath
                    )
                    db.session.add(entry)

                entries.append(entry)
    
        db.session.commit()
        logging.info(f'Stored {len(entries)} sequences from {filepath} in the database')
        return entries

    except IOError as e:
        raise ValueError(f'Failed to read the FASTA file: {e}')
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f'Failed to store sequences in the database: {e}')
    except Exception as e:
        db.session.rollback()
        raise ValueError(f'An unexpected error occurred: {e}')