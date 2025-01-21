"""
This module contains functions for generating visualizations of biological sequence data.

Functions:
- pie_plot: Generates a pie chart for nucleotide frequencies.
- bar_plot: Creates a bar chart for amino acid frequencies.
- gc_plot: Produces a line plot for GC content across a given sequence.
"""
import matplotlib
import base64
import io
import matplotlib.pyplot as plt

# Set global font size for all plots
plt.rcParams.update({'font.size': 20})

# Set a matplotlib backend
matplotlib.use('Agg')

def _set_plot_styling(ax, title):
    """Sets the common styling for all plots."""
    ax.set_title(title, wrap=True, color='white', pad=20)
    ax.tick_params(labelcolor='white')
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')


def _plot_to_base64(fig):
    """Converts a matplotlib figure to a base64-encoded PNG image."""
    img = io.BytesIO()
    fig.savefig(img, format='png', transparent=True, dpi=100)
    img.seek(0)
    plot_url = base64.b64encode(img.read()).decode()
    plt.close(fig)
    return f'data:image/png;base64,{plot_url}'

def pie_plot(header, nuc_freq):
    """
    Generates a pie chart visualization for nucleotide frequencies annotated with percentages. The chart represents
    the distribution of nucleotide frequencies and is titled with the provided header.

    The function saves the plot into a transparent PNG image file, encodes it in base64, and returns the encoded
    string suitable for embedding in HTML or other formats that support base64 encoded images.

    :param header: The title for the pie chart, typically describing the context of the nucleotide frequencies.
    :type header: str
    :param nuc_freq: A dictionary where keys are nucleotide characters (e.g., 'A', 'C', 'G', 'T') and values are
        their respective frequencies.
    :type nuc_freq: dict
    :return: A base64 encoded representation of the generated pie chart as a PNG image.
    :rtype: str
    """
    fig, ax = plt.subplots(figsize=(12, 7.5))
    nucleotides = list(nuc_freq.keys())
    frequencies = list(nuc_freq.values())

    ax.pie(frequencies, labels=nucleotides, autopct='%1.1f%%')
    _set_plot_styling(ax, f'Nucleotide Frequencies for {header}')

    return _plot_to_base64(fig)

def bar_plot(header, amino_freq):
    """
    Generates a bar plot representing amino acid frequencies using the provided
    header and amino frequency data. This function creates a visually appealing
    bar plot with custom formatting and returns the plot as a base64-encoded
    image in the PNG format. This enables embedding the plot in web-based
    interfaces or other platforms requiring a base64 image string.

    :param header: The header text displayed in the title of the plot. Typically,
        this could be a descriptive label or identifier related to the data being
        plotted.
    :type header: str
    :param amino_freq: A dictionary where keys represent amino acid names or
        symbols, and values are their corresponding frequencies (in percentage).
    :type amino_freq: dict[str, float]
    :return: A string containing the base64-encoded representation of the generated
        PNG image. The image string can be used to display the plot in
        applications requiring inline image rendering.
    :rtype: str
    """
    # Create the bar plot
    fig, ax = plt.subplots(figsize=(12, 7.5))
    amino_acids = list(amino_freq.keys())
    frequencies = list(amino_freq.values())

    ax.bar(amino_acids, frequencies)
    ax.set_ylabel('Frequency (%)', color='white')
    ax.set_xlabel('Nucleotides', color='white')
    _set_plot_styling(ax, f'Amino acid frequencies for {header}')

    return _plot_to_base64(fig)

def gc_plot(header, sequence):
    """
    Generates a GC content plot for a given DNA sequence. The function calculates the
    cumulative GC content at each position in the sequence and produces a line plot
    to visualize the GC content evolution across the sequence. The generated plot
    is returned as a base64-encoded PNG image.

    :param header: The header or identifier for the DNA sequence. Used as the title
                   of the plot.
    :type header: str
    :param sequence: The DNA sequence for which the GC content will be calculated
                     and plotted. The sequence is expected to be a string containing
                     valid DNA nucleotides ('A', 'T', 'G', 'C', 'U').
    :type sequence: str
    :return: A string containing the base64-encoded PNG image of the GC content plot.
    :rtype: str
    """
    # Calculate gc_content at each position
    gc_content = []
    for i in range(1, len(sequence) + 1):
            gc_count = sequence[:i].count('G') + sequence[:i].count('C')
            gc_content.append(gc_count / i * 100)

    # Create line plot
    fig, ax = plt.subplots(figsize=(24, 6))
    ax.plot(gc_content)

    ax.set_title(f'GC content for {header}', wrap=True, color='white', pad=20)
    ax.set_ylabel('GC content (%)', color='white')
    ax.set_xlabel('Position in sequence', color='white')
    _set_plot_styling(ax, f'GC content for {header}')

    return _plot_to_base64(fig)