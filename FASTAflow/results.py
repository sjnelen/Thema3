"""
This module provides utility functions for analyzing DNA and protein sequences. 

It includes methods for calculating GC content, nucleotide frequency, and sequence length, as well as 
translating a DNA sequence into a protein sequence and calculating amino acid frequencies.
"""
__author__ = 'Sam Nelen'
__version__ = '2025.01.16'

from Bio.SeqUtils import gc_fraction
from Bio.Seq import Seq

def calculate_gc_content(sequence):
    """
    Calculate the GC content percentage of a given DNA sequence.

    This function computes the percentage of guanine (G) and cytosine (C)
    bases in a DNA sequence. The GC content is an indicator of the
    molecular composition of the DNA. It returns 0.0 if the input
    sequence is empty.

    :param sequence: The DNA sequence for which the GC content is to be calculated.
    :type sequence: str
    :return: The GC content percentage of the sequence rounded to two decimal places.
    :rtype: float
    """
    if not sequence:
        return 0.0 # Return 0 when sequence has no value

    return round(gc_fraction(sequence) * 100, 2)


def calculate_nucleotide_frequency(sequence):
    """
    Calculates the frequency of each nucleotide in a given DNA sequence. The frequency
    is computed as the proportion of each nucleotide in the sequence and is returned
    as a percentage rounded to two decimal places. If the input sequence is empty,
    an empty dictionary is returned.

    :param sequence: The DNA sequence for which nucleotide frequency
                     needs to be calculated.
                     It should be a string consisting of nucleotide characters
                     ('A', 'T', 'G', 'C', 'U').
    :type sequence: str

    :return: A dictionary containing nucleotides as keys and their frequency
             in percentage as values.
    :rtype: dict
    """
    seq_len = len(sequence)
    if seq_len == 0:
        return {} # Return emtpy dictionary when length is 0

    counts = {}
    for nucleotide in sequence:
        counts[nucleotide] = counts.get(nucleotide, 0) + 1

    frequencies = {nuc : round((count / seq_len) * 100, 2) for nuc, count in counts.items()}
    return frequencies


def translate_to_protein(sequence):
    """
    Translates a nucleotide sequence to its corresponding protein sequence
    using the standard genetic code. Returns '?' for each amino acid in case
    of an error during translation.

    :param sequence: A nucleotide sequence to be translated.
    :type sequence: str
    :return: The translated protein sequence or a sequence of '?' characters
             of the same length as possible amino acids if an error occurs.
    :rtype: str
    """
    try:
        return str(Seq(sequence).translate())
    except Exception as e:
        print(f'Error translating sequence: {e}')
        return '?' * (len(sequence)//3)


def amino_acids_frequencies(protein_seq):
    """
    Calculates the frequencies of amino acids in a given protein sequence.

    This function takes a protein sequence as input and calculates the frequency
    of each amino acid within the sequence. The frequencies are given as a percentage
    of the total length of the protein sequence and rounded to two decimal places.

    :param protein_seq: The protein sequence for which amino acid frequencies need to
        be calculated.
    :type protein_seq: str
    :return: A dictionary where keys are amino acids and values are their respective
        frequencies in percentage.
    :rtype: dict
    """
    amino_counts = {}

    for amino in protein_seq:
        amino_counts[amino] = amino_counts.get(amino, 0) + 1

    frequencies = {amino : round(count / len(protein_seq) * 100, 2) for amino, count in amino_counts.items()}

    return frequencies








