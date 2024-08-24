"""
All the pages for the flask web application
"""
__author__ = 'Sam Nelen'
__version__ = '2024.08.22'

from flask import Blueprint, render_template, request
from app import ReadFasta

bp = Blueprint('pages', __name__)

ALLOWED_EXTENSIONS = {'fasta', 'fas', 'fa', 'fna', 'ffn', 'faa', 'mpfa', 'frn'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route("/")
def home():
    return render_template("home.html")

@bp.route("/about")
def about():
    return render_template("about.html")

@bp.route("/import_fasta")
def import_fasta():
    return render_template("import_fasta.html")

@bp.route("/upload", methods=['POST'])
def handle_upload():
    file = request.files['filename']
    if file and allowed_file(file.filename):
        file.save(f"temp/{file.filename}")
        filepath = f"temp/{file.filename}"
        headers = ReadFasta(filepath, None).get_headers()
        if len(headers) == 1:
            return render_template("fasta.html", filename=file.filename, headers=headers)
        elif len(headers) > 1:
            return "You uploaded a multi sequence FASTA file"
        else:
            return "Something is wrong with the fasta file, no header was found"
    else:
        # Need to implement an error page
        return f"invalid filetype: {file.filename}"