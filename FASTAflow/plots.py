"""Visualization module for sequence analysis results

This module provides plotting capabilities for visualizing multiple
sequence analysis results using matplotlib.

Typical usage example:
    plots = Plots(nucleotide_frequencies)
    pie_chart = plots.pie_chart(sequence_header)
    bar_chart = plots.bar_chart(sequence_header)
"""

__author__ = 'Sam Nelen'
__version__ = '2024.08.22'

import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
from read_fasta import ReadFasta


class Plots:
    """Creates visualization plots

    Attributes:
        nuc_freq (dict): Dictionary of nucleotide frequencies
    """

    def __init__(self, nuc_freq):
        """Initializes the Plots class

        Args:
            nuc_freq (dict): Dictionary of nucleotide frequencies
        """

        self.nuc_freq = nuc_freq

    def bar_plot(self, header):
        """Creates a bar chart

        Args:
            header (str): Sequence header to use as the plot title

        Returns:
            str: Filename of the saved plot

        Raises:
            OSError: If unable to save the plot
        """

        nuc_freq = self.nuc_freq
        plt.rcParams.update({'font.size': 20})

        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 7.5))
        nucleotides = list(nuc_freq.keys())
        frequencies = list(nuc_freq.values())

        ax.bar(nucleotides, frequencies)
        ax.set_ylabel('Frequency (%)', color='white')
        ax.set_xlabel('Nucleotides', color='white')
        ax.set_title(f'Nucleotide Frequencies for {header}', wrap=True, color='white', pad=20)
        ax.tick_params(labelcolor='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')

        # Safe the plot
        safe_header = secure_filename(f'{header.split()[0]}_bar_plot.png')  # Ensure filename is safe
        plt.savefig(f'FASTAflow/static/plots/{safe_header}', dpi=150, transparent=True)
        plt.close()

        return safe_header

    def pie_plot(self, header):
        """Creates a pie chart

        Args:
            header (str): Sequence header to use as the plot title

        Returns:
            str: Filename of the saved plot

        Raises:
            OSError: If unable to save the plot
        """
        nuc_freq = self.nuc_freq
        plt.rcParams.update({'font.size': 20})

        fig, ax = plt.subplots(figsize=(12, 7.5))
        nucleotides = list(nuc_freq.keys())
        frequencies = list(nuc_freq.values())

        ax.pie(frequencies, labels=nucleotides, autopct='%1.1f%%')
        ax.set_title(f'Nucleotide Frequencies for {header}', wrap=True, color='white', pad=20)

        # Safe the plot
        safe_header = secure_filename(f'{header.split()[0]}_pie_plot.png')  # Ensure filename is safe
        plt.savefig(f'FASTAflow/static/plots/{safe_header}', dpi=150, transparent=True)
        plt.close()

        return safe_header

    def gc_plot(self, header, filepath):
        seq_dict = ReadFasta(filepath).read_file()
        sequence = seq_dict[header]

        gc_content = []

        # Calculate gc_content at each position
        for i in range(len(sequence) + 1):
            if i > 0: # Avoid dividing by 0
                gc_count = sequence[:i].count('G') + sequence[:i].count('C')
                gc_content.append(gc_count / i * 100)
            else:
                gc_content.append(0)

        # Create line plot
        fig, ax = plt.subplots(figsize=(24, 6))
        ax.plot(gc_content)
        ax.set_title(f'GC content for {header}', wrap=True, color='white', pad=20)
        ax.set_ylabel('GC content (%)', color='white')
        ax.set_xlabel('Position in sequence', color='white')
        ax.tick_params(labelcolor='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')

        safe_header = secure_filename(f'{header.split()[0]}_gc_plot.png')  # Ensure filename is safe
        plt.savefig(f'FASTAflow/static/plots/{safe_header}', dpi=150, transparent=True)
        plt.close()

        return safe_header
