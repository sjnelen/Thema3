"""Page routing and request handling for the application

This module contains all the route definitions and request handlers for the
web application. It controls the file uploads, processing, and result
visualization.

Example:
    bp = Blueprint('pages', __name__)
"""

__author__ = 'Sam Nelen'
__version__ = '2024.08.22'

from flask import Blueprint, render_template, request, abort, session, redirect, url_for
import os

from werkzeug.utils import secure_filename

from FASTAflow.models import db, FastaEntry
from read_fasta import ReadFasta
from results import Results
from plots import Plots

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

@bp.route('/analyse_again')
def analyse_again():
    db.session.query(FastaEntry).delete()
    db.session.commit()
    return redirect(url_for('pages.import_fasta'))


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
        headers = ReadFasta(filepath).get_headers()
        seq_dict = ReadFasta(filepath).read_file()

        for header in headers:
            entry = FastaEntry(
                header=header,
                filepath=filepath)
            db.session.add(entry)
        db.session.commit()

        entries = FastaEntry.query.filter_by(filepath=filepath).all()

        if entries:
            return render_template('fasta.html', entries=entries, seq_dict=seq_dict)
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
        analysis_options = request.form.getlist('analysis_options')
        session['analysis_options'] = analysis_options
    else:
        analysis_options = session.get('analysis_options')

    # Get the latest entry in the database
    latest_entry = FastaEntry.query.order_by(FastaEntry.id.desc()).first()
    if not latest_entry:
        abort(400, description="No entry was found in the database")

    # Get the filepath and filter the headers based on the filepath
    filepath = latest_entry.filepath

    # Get the sequence from the file and run the analysis based on the chosen options
    seq_dict = ReadFasta(filepath).read_file()
    results = Results(analysis_options, seq_dict)
    results.run_analysis()

    protein_sequences = results.protein_translation()

    entries = FastaEntry.query.filter_by(filepath=filepath).all()

    return render_template('results.html',
                           options=analysis_options, protein=protein_sequences, entries=entries)


@bp.route('/plots/<header>')
def plots(header):
    #Get the entry in the database based on the header
    entry = FastaEntry.query.filter_by(header=header).first()

    #Get the different nucleotide frequencies
    nuc_freq = entry.nuc_freq
    filepath = entry.filepath

    #Create the plots
    graphs = Plots(nuc_freq)
    pie_plot_filename = graphs.pie_plot(header)
    bar_plot_filename = graphs.bar_plot(header)
    gc_plot_filename = graphs.gc_plot(header, filepath)

    return render_template('plots.html',
                           header=header,
                           pie_plot_filename = pie_plot_filename,
                           bar_plot_filename = bar_plot_filename,
                           gc_plot_filename = gc_plot_filename)
