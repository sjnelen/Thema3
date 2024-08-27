"""
All the function that are performed in the background
"""
__author__ = 'Sam Nelen'
__version__ = '2024.08.22'

class ReadFasta:

    def __init__(self, file):
        self.file = file
        self.headers = []
        self.fasta_dict = {}


    def get_headers(self):
        """
        Opens the file and loops over every line, where the lines starting with a '>'
        are put in the headers lis
        :return: The headers list
        """
        with open(self.file, 'r') as f:
            for line in f:
                if line.startswith('>'):
                    self.headers.append(line.strip())

        return self.headers
    
    def read_file(self):
        """
        Reads the fasta file and pairs the header and sequence in a dictionary
        :return: The dictionary of headers and sequence
        """
        with open(self.file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    current_header = line
                    self.fasta_dict[current_header] = ''
                else:
                    self.fasta_dict[current_header] += line

        return self.fasta_dict




