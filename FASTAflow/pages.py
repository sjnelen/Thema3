"""
All the pages for the flask web application
"""
__author__ = 'Sam Nelen'
__version__ = '2024.08.22'

from flask import Blueprint, render_template, request, session, abort
import os

from werkzeug.utils import secure_filename

from read_fasta import ReadFasta
from results import Results

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
        seq_dict = ReadFasta(filepath).read_file()
        session['seq_dict'] = seq_dict
        if len(headers) == 1:
            return render_template('fasta.html',
                                   filename=file.filename, headers=headers, seq_dict=seq_dict)
        elif len(headers) > 1:
            return render_template('multi_fasta.html',
                                   filename=file.filename, headers=headers, seq_dict=seq_dict)
        else:
            # Need to implement an error page
            return 'Something is wrong with the fasta file, no header was found'
    else:
        # Need to implement an error page
        return f'invalid filetype: {file.filename}'


@bp.route('/result', methods=['POST'])
def result():
    analysis_options = request.form.getlist('analysis_options')
    seq_dict = session.get('seq_dict')
    results = Results(analysis_options, seq_dict).run_analysis()
    return render_template('results.html', results=results)
