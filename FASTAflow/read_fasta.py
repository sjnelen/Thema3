"""FASTA file parsing module for the FASTAflow application

This module provides the functionality for reading and parsing FASTA
format files. It extracts the headers and sequences

Typical usage example:
    reader = ReadFasta('path/to/file.fasta')
    headers = reader.get_headers()
    sequences = reader.read_file()
"""

__author__ = 'Sam Nelen'
__version__ = '2024.08.22'

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
                entry = FastaEntry(
                    id=record.id,
                    description=record.description,
                    sequence=str(record.seq),
                    filepath=filepath
                )
                entries.append(entry)
                db.session.add(entry)
    
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