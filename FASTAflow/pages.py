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
from flask import Blueprint, render_template, request, abort, session, redirect, url_for

import os
import glob
from werkzeug.utils import secure_filename
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
    """Handles the FASTA file uploads and processes them

    Processes the uploaded file by:
    1. Validating the file type
    2. Saving to a temporary location
    3. Extracting the headers
    4. Storing in the database

    Returns:
        str: Rendered HTML template with headers or error message.

    Raises:
        werkzeug.exceptions.BadRequest: If there is no file uploaded.
    """

    # Clear the session so no 'analysis_option' is present
    session.clear()

    if 'fastaFile' not in request.files:
        abort(400, description="No file part in the request.")

    file = request.files['fastaFile']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join('temp', filename)
        file.save(filepath)

        store_fasta_in_db(filepath)

        entries = FastaEntry.query.all()

        if entries:
            return render_template('fasta.html', entries=entries)
        else:
            # Need to implement an error page
            return 'Something is wrong with the fasta file, no headers were found'
    else:
        # Need to implement an error page
        return f'invalid filetype: {file.filename}'


@bp.route('/result', methods=['POST', 'GET'])
def result():
    # Store the analysis options in a session
    if request.method == 'POST':
        selected_sequences = request.form.getlist('selected_sequences')
        session['selected_sequences'] = selected_sequences
    else:
        selected_sequences = session.get('selected_sequences')

    entries = FastaEntry.query.filter(FastaEntry.id.in_(selected_sequences)).all()

    for entry in entries:
        seq = Seq(entry.sequence)

        entry.gc_content = results.calc_gc_content(seq)
        entry.nuc_freq = results.calc_nucleotide_frequency(seq)
        entry.sequence_length = results.calc_sequence_length(seq)
        entry.protein_seq = results.translate_to_protein(seq)

        db.session.commit()

    return render_template('results.html', entries=entries)


@bp.route('/plots/<header>')
def plots(header):
    #Get the entry in the database based on the header
    entry = FastaEntry.query.filter_by(description=header).first()

    #Get the nucleotide frequencies and the sequence
    nuc_freq = entry.nuc_freq
    sequence = entry.sequence

    #Create the plots
    pie_plot_filename = graphs.pie_plot(header, nuc_freq)
    bar_plot_filename = graphs.bar_plot(header, nuc_freq)
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