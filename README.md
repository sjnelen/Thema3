# FASTAflow 

## Description
FASTAflow is a small web application that allows users to upload and analyse small 
FASTA files. When the analysis is finished the web application will show some results 
and plots about a few stats to the user.

## Features
* Upload and parse FASTA files
* Calculate GC content
* Analyze nucleotide frequencies
* Determine sequence length
* Translate a protein sequence
* Visualize some stats in plots

## Installation
For running the flask app from the commandline the following commands set up a starting
point for development. When the last command is executed a webserver will be started 
binding to `localhost` on `127.0.0.1`. Then the website can be visited when going to the
following url: `http://localhost:8000` in your browser.

1. Clone the repository: `git clone 'https://github.com/sjnelen/Thema3.git'`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python -m FASTAflow`

## Acknowledgments  
FASTAflow is built with the help of several open-source tools and libraries.

- **[Biopython](https://biopython.org/)**: Essential for parsing FASTA files and performing biological sequence operations.  
- **[Flask](https://flask.palletsprojects.com/)**: A lightweight web framework for building the application.  
- **[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)** and **[SQLAlchemy](https://www.sqlalchemy.org/)**: 
For seamless database integration and management.  
- **[Flask-Migrate](https://flask-migrate.readthedocs.io/)**: To handle database migrations effortlessly.  
- **[Matplotlib](https://matplotlib.org/)**: For generating visualizations and plots.  
- **[NumPy](https://numpy.org/)**: For efficient numerical computations.  
- **[Jinja2](https://palletsprojects.com/p/jinja/)**: Used as the templating engine to render dynamic web pages.

## Development in the Pycharm ide
To set up a IDE follow the steps below for the IDE of my choice Pycharm. 
1. **Clone the repository**
   * Open pycharm and select **File > New project > Get from version control**
   * Paste the repository url `https://github.com/sjnelen/Thema3.git`

2. **Set Up a Virtual Environment, if not done automatically**  
   - Navigate to **File > Settings > Python Interpreter** (or **Preferences** on macOS).  
   - Click the gear icon, then select **Add Interpreter > Add Local Interpreter > Virtual Environment**.  
   - Point to the `venv` folder if it's already created, or let PyCharm create a new one in the project directory.  

3. **Install Dependencies**  
   - Open the terminal in PyCharm (or use the PyCharm interface to manage dependencies).  
   - Run: `pip install -r requirements.txt`

4. **Set up the flask run configuration**
   - Go to **Run > Edit configurations** 
   - Click the **+** icon to add a new configuration and select **Python**
   - Instead of **script** select the **module** option, and type in **FASTAflow**
   - Hit apply and now you can start the server from Pycharm

## Working with flask-migrate
Flaks migrate is a useful tool when a database is in use with the flask application. Especially when the application
is run in production. When the database undergoes changes the flask-migrate tool helps with migrating the database 
schema without losing data. All the documentation can be found on their site which can be found in the Acknowledgments
section

## Contacts
Name: Sam Nelen  
Email: s.j.nelen@st.hanze.nl  
Organization: [Hanze Hogeschool](https://www.hanze.nl/nl) 

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
