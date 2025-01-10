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

from FASTAflow.models import db, FastaEntry


def store_fasta_in_db(file):
  """Reads and parses the FASTA file.

  Args:
      file: Path to the FASTA file.

  Returns:
      list: List of Bio.SeqRecord objects representing the sequences in the FASTA file.

  Raises:
      IOError: If the FASTA file cannot be opened or read.
  """
  with open(file, 'r') as file_handle:
        for record in SeqIO.parse(file_handle, 'fasta'):
            entry = FastaEntry (
                id = record.id,
                description = record.description,
                sequence = str(record.seq),
                filepath = file
            )
            db.session.add(entry)

        try:
            db.session.commit()
            print('FASTA file stored in database')
        except Exception as e:
            db.session.rollback()
            print(f'Error storing FASTA file in database: {e}')




