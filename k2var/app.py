from flask import Flask, render_template
from os import path

BASE_DIR = path.realpath(
    path.join(
        path.dirname(__file__), '..'))

app = Flask(__name__)
app.config['FREEZER_BASE_URL'] = 'http://localhost/'
app.config['FREEZER_DESTINATION'] = path.join(BASE_DIR, 'build')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

