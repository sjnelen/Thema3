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

class ReadFasta:
    """FASTA file parser class

    Attributes:
        file (str): Path to the FASTA file.
        headers (list): List to store the sequence headers.
        fasta_dict (dict): Dictionary to store header-sequence pairs.
    """

    def __init__(self, file):
        """Initializes the ReadFasta class.

        Args:
            file (str): Path to the FASTA file.
        """
        self.file = file
        self.headers = []
        self.fasta_dict = {}


    def get_headers(self):
        """Extract the headers from the FASTA file.

        Returns:
            list: List of sequence headers.

        Raises:
            IOError: If the FASTA file cannot be opened or read.
        """
        with open(self.file, 'r') as f:
            for line in f:
                if line.startswith('>'):
                    self.headers.append(line.strip())

        return self.headers
    
    def read_file(self):
        """Reads and parses the FASTA file.

        Returns:
            dict: Dictionary with the headers as keys and sequences as values.

        Raises:
            IOError: If the FASTA file cannot be opened or read.
        """
        current_header = None
        with open(self.file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    current_header = line
                    self.fasta_dict[current_header] = ''
                elif current_header:
                    self.fasta_dict[current_header] += line

        return self.fasta_dict




