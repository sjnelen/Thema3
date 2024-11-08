"""
All the plots that are needed to show the results
"""
__author__ = 'Sam Nelen'
__version__ = '2024.08.22'

import matplotlib.pyplot as plt
import numpy as np

class Plots:

    def __init__(self, results):
        self.results = results

    def bar_plot(self):
        nuc_freq = self.results['nuc_freq']

        nucleotides = list(next(iter(nuc_freq.values())).keys())
        headers = list(nuc_freq.keys())

        x = np.arange(len(headers))
        width = 0.2

        fig, ax = plt.subplots(figsize=(12, 6))

        for i, nuc in enumerate(nucleotides):
            frequencies = [nuc_freq[header][nuc] for header in headers]
            ax.bar(x + i*width, frequencies, width, label=nuc)

        ax.set_ylabel('Frequency')
        ax.set_title('Nucleotide Frequencies by Sequence')
        ax.set_xticks(x + width * (len(nucleotides) - 1) / 2)
        ax.legend()

        plt.tight_layout()
        plt.savefig('FASTAflow/static/plots/bar_plot.png')
        plt.close()
