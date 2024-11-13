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
import numpy as np
from werkzeug.utils import secure_filename


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
