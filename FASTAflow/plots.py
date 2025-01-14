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

import base64
import io

import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename

def pie_plot(header, nuc_freq):
    """Creates a pie chart

    Args:
        header (str): Sequence header to use as the plot title
        nuc_freq (dict): Dictionary of nucleotide frequencies

    Returns:
        str: Filename of the saved plot

    Raises:
        OSError: If unable to save the plot
    """
    plt.rcParams.update({'font.size': 20})

    fig, ax = plt.subplots(figsize=(12, 7.5))
    nucleotides = list(nuc_freq.keys())
    frequencies = list(nuc_freq.values())

    ax.pie(frequencies, labels=nucleotides, autopct='%1.1f%%')
    ax.set_title(f'Nucleotide Frequencies for {header}', wrap=True, color='white', pad=20)

    img = io.BytesIO()
    plt.savefig(img, format='png', transparent=True, dpi=150)
    img.seek(0)
    plot_url = base64.b64encode(img.read()).decode()
    plt.close()

    return f"data:image/png;base64,{plot_url}"

def bar_plot(header, protein_seq):
    """Creates a bar chart

    Args:
        header (str): Sequence header to use as the plot title
        nuc_freq (dict): Dictionary of nucleotide frequencies

    Returns:
        str: Filename of the saved plot

    Raises:
        OSError: If unable to save the plot
    """
    amino_counts = {}

    for amino in protein_seq:
        amino_counts[amino] = amino_counts.get(amino, 0) + 1

    frequencies = {amino : round(count / len(protein_seq) * 100, 2) for amino, count in amino_counts.items()}

    plt.rcParams.update({'font.size': 20})

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 7.5))

    amino = list(frequencies.keys())
    frequencies = list(frequencies.values())

    ax.bar(amino, frequencies)
    ax.set_ylabel('Frequency (%)', color='white')
    ax.set_xlabel('Nucleotides', color='white')
    ax.set_title(f'Amino acid Frequencies for {header}', wrap=True, color='white', pad=20)
    ax.tick_params(labelcolor='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

    img = io.BytesIO()
    plt.savefig(img, format='png', transparent=True, dpi=150)
    img.seek(0)
    plot_url = base64.b64encode(img.read()).decode()
    plt.close()

    return f"data:image/png;base64,{plot_url}"

def gc_plot(header, sequence):
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

    img = io.BytesIO()
    plt.savefig(img, format='png', transparent=True, dpi=150)
    img.seek(0)
    plot_url = base64.b64encode(img.read()).decode()
    plt.close()

    return f"data:image/png;base64,{plot_url}"