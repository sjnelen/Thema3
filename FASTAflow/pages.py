"""
Module handling routes and functionality for a Flask-based web application.

This module includes view functions for rendering pages, handling uploaded FASTA files, 
processing data, and generating results/plots. It interacts with a database to store 
fasta file contents and computes various analyses including GC content, nucleotide frequency, 
sequence translation, and analysis plots.
"""
__author__ = 'Sam Nelen'
__version__ = '2025.01.16'

from Bio.Seq import Seq
from flask import Blueprint, render_template, request, session
import os
from werkzeug.utils import secure_filename
import logging

import results
import plots as graphs
from FASTAflow.models import db, FastaEntry
from read_fasta import store_fasta_in_db

bp = Blueprint('pages', __name__)

ALLOWED_EXTENSIONS = {'fasta', 'fas', 'fa', 'fna', 'ffn', 'faa', 'mpfa', 'frn'}


def allowed_file(filename):
    """
    Check if a file has an allowed extension.

    This function determines if a given filename corresponds to a file
    with an extension from the list of allowed extensions. It checks for
    the presence of a file extension and validates it against a predefined
    list of allowed extensions.

    :param filename: A string representing the name of the file whose
        extension needs to be validated.
    :returns: A boolean value indicating whether the given file extension
        is allowed or not.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/')
def home():
    """
    Route handler for the '/' endpoint, rendering the 'home.html' template.

    :return: Rendered HTML content of the home page.
    """
    return render_template('home.html')


@bp.route('/about')
def about():
    """
    Route handler for the '/about' endpoint, rendering the 'about.html' template.

    :return: Rendered HTML content of the 'about' page.
    """
    return render_template('about.html')


@bp.route('/import_fasta')
def import_fasta():
    """
    Route handler for the '/import_fasta' endpoint, rendering the 'import_fasta.html' template.

    :return: Rendered HTML content of the 'import_fasta' page.
    """
    return render_template('import_fasta.html')


@bp.route('/upload', methods=['POST'])
def handle_upload():
    """
    Handles the upload of a FASTA file via a POST request. Validates the request,
    processes the uploaded file, and parses its contents to store in the database.

    :returns: An HTML page rendered with results or error messages depending on 
        the success or failure of the upload and processing.

    :raises ValueError: If the file processing encounters invalid data or fails
        to extract any sequences.
    :raises IOError: If saving the uploaded file to disk fails due to I/O issues.
    :raises Exception: For unexpected errors during file processing.
    """
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

            return render_template('choose_seq.html', entries=entries)

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
    """
    Handles the processing and rendering of the 'result' endpoint. Depending on the HTTP
    method, either processes data submitted via a POST request or retrieves data via a GET
    request. In the case of a POST request, analyzes sequences submitted by users and updates
    the database with calculated metrics. For a GET request, fetches the sequences previously
    selected by the user from the session. Ultimately, renders the 'results.html' template with
    the processed data.

    :return: Renders the 'results.html' template along with processed sequence entries or
             the previously selected entries.
    """
    if request.method == 'POST':
        selected_sequences = request.form.getlist('selected_sequences')
        session['selected_sequences'] = selected_sequences

        entries = db.session.query(FastaEntry).id.in_(selected_sequences).all()

        # Run al the analysis
        for entry in entries:
            seq = Seq(entry.sequence)

            entry.gc_content = results.calculate_gc_content(seq)
            entry.nuc_freq = results.calculate_nucleotide_frequency(seq)
            entry.sequence_length = results.calculate_sequence_length(seq)
            entry.protein_seq = results.translate_to_protein(seq)

        db.session.commit()
    else:
        selected_sequences = session.get('selected_sequences')
        entries = db.session.query(FastaEntry).id.in_(selected_sequences).all()

    return render_template('results.html', entries=entries)


@bp.route('/plots/<header>')
def plots(header):
    """
    Generates and returns various plots for a given database entry based on the
    provided header. The function retrieves the entry from the database, computes
    nucleotide and amino acid frequencies, and creates corresponding visualizations
    for rendering on a web page. The generated plots include a pie chart for
    nucleotide frequencies, a bar chart for amino acid frequencies, and a GC-content
    plot.

    :param header: The sequence header used to query the database for a
        corresponding `FastaEntry`.
    :type header: str
    :return: Rendered HTML template displaying the generated plots for the given
        `header`.
    """
    #Get the entry in the database based on the header
    entry = db.session.query(FastaEntry).filter_by(description=header).first()

    sequence = entry.sequence
    nuc_freq = entry.nuc_freq
    amino_freq = results.amino_acids_frequencies(entry.protein_seq)

    pie_plot = graphs.pie_plot(header, nuc_freq)
    bar_plot = graphs.bar_plot(header, amino_freq)
    gc_plot = graphs.gc_plot(header, sequence)

    return render_template('plots.html',
                           header=header,
                           pie_plot = pie_plot,
                           bar_plot = bar_plot,
                           gc_plot = gc_plot)