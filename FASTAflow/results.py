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
    """Calculates the GC content of the sequences.

    Updates the database with GC content percentages for each sequence.
    """
    if not sequence:
        return 0.0 # Return 0 when sequence has no value

    return round(gc_fraction(sequence) * 100, 2)

def calculate_nucleotide_frequency(sequence):
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

def calculate_sequence_length(sequence):
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

def amino_acids_frequencies(protein_seq):
    amino_counts = {}

    for amino in protein_seq:
        amino_counts[amino] = amino_counts.get(amino, 0) + 1

    frequencies = {amino : round(count / len(protein_seq) * 100, 2) for amino, count in amino_counts.items()}

    return frequencies








