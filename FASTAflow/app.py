"""
All the function that are performed in the background
"""
__author__ = 'Sam Nelen'
__version__ = '2024.08.22'

class ReadFasta:
    file = None
    headers = None

    def __init__(self, file, headers):
        self.file = file
        self.headers = []


    def get_headers(self):
        with open(self.file, 'r') as f:
            for line in f:
                if line.startswith('>'):
                    self.headers.append(line.strip())

        return self.headers

