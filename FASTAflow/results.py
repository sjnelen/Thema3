"""Sequence analysis module for the FASTAflow application

This module provides various sequence analysis functions including GC content
calculations, nucleotide frequency analysis, sequence length calculations,
and protein translation.

Typical usage example:
    analyzer = Results(['gc_content', 'seq_length'], sequences)
    results = analyzer.run_analysis()
"""
__author__ = 'Sam Nelen'
__version__ = '2024.08.22'


from Bio.SeqUtils import gc_fraction
from Bio.Seq import Seq
from collections import Counter

def calc_gc_content(sequence):
    """Calculates the GC content of the sequences.

    Updates the database with GC content percentages for each sequence.
    """

    if not sequence:
        return 0.0

    return round(gc_fraction(sequence) * 100, 2)

def calc_nucleotide_frequency(sequence):
    """Calculates the nucleotide frequency of the sequences.

    Updates the database with nucleotide frequency for each sequence.
    """
    seq_len = len(sequence)
    if seq_len == 0:
        return {} # Return emtpy dictionary when length is 0

    counts = {}
    for nucleotide in sequence:
        counts[nucleotide] = counts.get(nucleotide, 0) + 1

    frequencies = {nuc : round((count / seq_len) * 100, 2) for nuc, count in counts.items()}
    return frequencies

def calc_sequence_length(sequence):
    """Calculates the sequence length of the sequences.

    Updates the database with sequence length for each sequence.
    """
    return len(sequence)

def translate_to_protein(sequence):
    try:
        return str(Seq(sequence).translate())
    except Exception as e:
        print(f'Error translating sequence: {e}')
        return '?' * (len(sequence)//3)








