"""Page routing and request handling for the application

This module contains all the route definitions and request handlers for the
web application. It controls the file uploads, processing, and result
visualization.

Example:
    bp = Blueprint('pages', __name__)
"""

__author__ = 'Sam Nelen'
__version__ = '2024.08.22'

from Bio.Seq import Seq
from flask import Blueprint, render_template, request, session, redirect, url_for
import os
import glob
from werkzeug.utils import secure_filename
import logging

import results
import plots as graphs
from FASTAflow.models import db, FastaEntry
from read_fasta import store_fasta_in_db

bp = Blueprint('pages', __name__)

ALLOWED_EXTENSIONS = {'fasta', 'fas', 'fa', 'fna', 'ffn', 'faa', 'mpfa', 'frn'}


def allowed_file(filename):
    """Validates if the uploaded file has a FASTA extension.

    Args:
        filename (string): The name of the uploaded file.

    Returns:
        bool: True if the file extension is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/import_fasta')
def import_fasta():
    return render_template('import_fasta.html')


@bp.route('/upload', methods=['POST'])
def handle_upload():
    try:
        # Clear the session for new uploads
        session.clear()

        # Make sure the request is correct and a correct file is uploaded
        if 'fastaFile' not in request.files:
            return render_template('error.html',
                                   error='The FASTA file was not found in the request')

        file = request.files['fastaFile']
        if not file.filename:
            return render_template('error.html',
                                   error='No file selected for upload, please choose a file before proceeding')

        if not allowed_file(file.filename):
            return render_template('error.html',
                                   error=f'Invalid file type: {file.filename}, please choose a FASTA file')

        # Create temporary file for processing
        filename = secure_filename(file.filename)
        fasta_filepath = os.path.join('temp', filename)
        os.makedirs('temp', exist_ok=True)

        # Save the file
        try:
            file.save(fasta_filepath)
        except IOError as e:
            logging.error(f'Failed to save the uploaded file: {e}')
            return render_template('error.html',
                                   error='Failed to save the uploaded file, please try again'), 500

        try:
            entries = store_fasta_in_db(fasta_filepath)
            os.remove(fasta_filepath)

            if not entries:
                return render_template('error.html',
                                       error='No sequences were found in the file'), 400

            return render_template('fasta.html', entries=entries)

        except ValueError as e:
            logging.error(f'Failed to process the uploaded file: {e}')
            return render_template('error.html',
                                   error='Failed to process the uploaded file, please try again'), 500
        except Exception as e:
            logging.error(f'An unexpected error occurred: {e}')
            return render_template('error.html',
                                   error='An unexpected error occurred, please try again'), 500

    finally:
        if 'fastaFile' in locals() and os.path.exists(fasta_filepath):
            os.remove(fasta_filepath)


@bp.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        selected_sequences = request.form.getlist('selected_sequences')
        session['selected_sequences'] = selected_sequences

        entries = FastaEntry.query.filter(FastaEntry.id.in_(selected_sequences)).all()

        for entry in entries:
            seq = Seq(entry.sequence)

            entry.gc_content = results.calc_gc_content(seq)
            entry.nuc_freq = results.calc_nucleotide_frequency(seq)
            entry.sequence_length = results.calc_sequence_length(seq)
            entry.protein_seq = results.translate_to_protein(seq)
    else:
        selected_sequences = session.get('selected_sequences')
        entries = FastaEntry.query.filter(FastaEntry.id.in_(selected_sequences)).all()


    db.session.commit()

    return render_template('results.html', entries=entries)


@bp.route('/plots/<header>')
def plots(header):
    #Get the entry in the database based on the header
    entry = FastaEntry.query.filter_by(description=header).first()

    sequence = entry.sequence
    nuc_freq = entry.nuc_freq
    protein_seq = entry.protein_seq

    pie_plot_filename = graphs.pie_plot(header, nuc_freq)
    bar_plot_filename = graphs.bar_plot(header, protein_seq)
    gc_plot_filename = graphs.gc_plot(header, sequence)

    return render_template('plots.html',
                           header=header,
                           pie_plot_filename = pie_plot_filename,
                           bar_plot_filename = bar_plot_filename,
                           gc_plot_filename = gc_plot_filename)


@bp.route('/analyse_again')
def analyse_again():
    # Empty the database with analysis results for a new run
    db.session.query(FastaEntry).delete()
    db.session.commit()

    # Delete the plot images from the folder
    plot_path = 'FASTAflow/static/plots/'
    for file in glob.glob(plot_path + '*.png'):
        os.remove(file)

    return redirect(url_for('pages.import_fasta'))