"""
All the plots that are needed to show the results
"""
__author__ = 'Sam Nelen'
__version__ = '2024.08.22'

import matplotlib.pyplot as plt
import numpy as np
from werkzeug.utils import secure_filename


class Plots:

    def __init__(self, nuc_freq):
        self.nuc_freq = nuc_freq

    def bar_plot(self, header):
        nuc_freq = self.nuc_freq
        plt.rcParams.update({'font.size': 20})

        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 6))
        nucleotides = list(nuc_freq.keys())
        frequencies = list(nuc_freq.values())

        ax.bar(nucleotides, frequencies)
        ax.set_ylabel('Frequency (%)')
        ax.set_xlabel('Nucleotides')
        ax.set_title(f'Nucleotide Frequencies for {header}', wrap=True)

        # Safe the plot
        safe_header = secure_filename(f'{header.split()[0]}_bar_plot.png')  # Ensure filename is safe
        plt.savefig(f'FASTAflow/static/plots/{safe_header}', dpi=300)
        plt.close()

        return safe_header

    def pie_plot(self, header):
        nuc_freq = self.nuc_freq
        plt.rcParams.update({'font.size': 20})

        fig, ax = plt.subplots(figsize=(12, 6))
        nucleotides = list(nuc_freq.keys())
        frequencies = list(nuc_freq.values())

        ax.pie(frequencies, labels=nucleotides, autopct='%1.1f%%')
        ax.set_title(f'Nucleotide Frequencies for {header}', wrap=True)

        # Safe the plot
        safe_header = secure_filename(f'{header.split()[0]}_pie_plot.png')  # Ensure filename is safe
        plt.savefig(f'FASTAflow/static/plots/{safe_header}', dpi=300)
        plt.close()

        return safe_header
