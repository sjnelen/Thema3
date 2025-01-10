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

from FASTAflow.models import db, FastaEntry


class Results:
    """Sequence analysis class for various analysis methods

    Attributes:
        options (list): List of selected analysis options.
        seq_dict (dict): Dictionary of sequences to analyze.
        results (dict): Dictionary to store sequence analysis results
    """

    def __init__(self, options, seq_dict):
        """Initializes the results class

        Args:
            options (list): List of selected analysis options.
            seq_dict (dict): Dictionary of sequences to analyze.
        """

        self.options = options
        self.seq_dict = seq_dict
        self.results = {}

    def run_analysis(self):
        """Executes the selected analyze options

        Returns:
            dict: Dictionary of sequence analysis results.
        """

        if 'gc_content' in self.options:
            self.gc_content()
        if 'seq_length' in self.options:
            self.seq_length()
        if 'to_protein' in self.options:
            self.results['to_protein'] = self.protein_translation()
        if 'nuc_freq' in self.options:
            self.nucleotide_frequency()

        return self.results


    def gc_content(self):
        """Calculates the GC content of the sequences.

        Updates the database with GC content percentages for each sequence.
        """

        #gc_results = {}
        for header, seq in self.seq_dict.items():
            total = len(seq)
            g = seq.count('G')
            c = seq.count('C')
            #gc_results[header] = f'{(g+c)/total * 100:.2f} %'

            entry = FastaEntry.query.filter_by(header = header).first()
            entry.gc_content = round((g+c) / total * 100, 2)
            db.session.commit()

        return None

    def nucleotide_frequency(self):
        """Calculates the nucleotide frequency of the sequences.

        Updates the database with nucleotide frequency for each sequence.
        """
        #nuc_results = {}
        nuc_freq = {}
        for header, seq in self.seq_dict.items():
            for nuc in seq:
                nuc_freq[nuc] = round(nuc_freq.get(nuc, 0) + 1/len(seq) * 100, 2)
            #nuc_results[header] = nuc_freq

            entry = FastaEntry.query.filter_by(header = header).first()
            entry.nuc_freq = nuc_freq
            db.session.commit()

        return None


    def seq_length(self):
        """Calculates the sequence length of the sequences.

        Updates the database with sequence length for each sequence.
        """
        #length_result = {}
        for header, seq in self.seq_dict.items():
            length = len(seq)
            #length_result[header] = length

            entry = FastaEntry.query.filter_by(header = header).first()
            entry.sequence_length = length
            db.session.commit()

        return None


    def protein_translation(self):
        """Translates DNA sequences into protein sequences.

        Returns:
            dict: Dictionary with headers as keys and protein sequences as values.

        Note:
            Uses standard genetic code for translation.
            Unknown codons are represented with a '?'.
        """
        protein_result = {}
        aa_table = {
            'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
            'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
            'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
            'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
            'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
            'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
            'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
            'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
            'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
            'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
            'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
            'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
            'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
            'TAC': 'Y', 'TAT': 'Y', 'TAA': '*', 'TAG': '*',
            'TGC': 'C', 'TGT': 'C', 'TGA': '*', 'TGG': 'W',
        }

        for header, seq in self.seq_dict.items():
            amino_acid = ""
            for i in range(0,len(seq),  3):
                codon = seq[i:i+3]
                amino_acid += aa_table.get(codon, '?')

            protein_result[header] = amino_acid

        return protein_result

