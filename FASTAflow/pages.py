"""
All the pages for the flask web application
"""
__author__ = 'Sam Nelen'
__version__ = '2024.08.22'

from flask import Blueprint, render_template, request, abort
import os

from werkzeug.utils import secure_filename

from FASTAflow.models import db, FastaEntry
from read_fasta import ReadFasta
from results import Results
from plots import Plots

bp = Blueprint('pages', __name__)

ALLOWED_EXTENSIONS = {'fasta', 'fas', 'fa', 'fna', 'ffn', 'faa', 'mpfa', 'frn'}


def allowed_file(filename):
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
    if 'fastaFile' not in request.files:
        abort(400, description="No file part in the request.")

    file = request.files['fastaFile']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join('temp', filename)
        file.save(filepath)
        headers = ReadFasta(filepath).get_headers()
        #seq_dict = ReadFasta(filepath).read_file()

        for header in headers:
            entry = FastaEntry(
                header=header,
                filepath=filepath)
            db.session.add(entry)
        db.session.commit()

        entries = FastaEntry.query.filter_by(filepath=filepath).all()

        #session['seq_dict'] = seq_dict
        #session['headers'] = headers
        if entries:
            return render_template('fasta.html', headers=entries)
        else:
            # Need to implement an error page
            return 'Something is wrong with the fasta file, no headers were found'
    else:
        # Need to implement an error page
        return f'invalid filetype: {file.filename}'


@bp.route('/result', methods=['POST', 'GET'])
def result():
    # Get a list with the analysis options
    analysis_options = request.form.getlist('analysis_options')

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

    #Create the plots
    graphs = Plots(nuc_freq)
    pie_plot_filename = graphs.pie_plot(header)
    bar_plot_filename = graphs.bar_plot(header)

    return render_template('plots.html',
                           header=header,
                           pie_plot_filename = pie_plot_filename,
                           bar_plot_filename = bar_plot_filename)
