from app import app
from flask.templating import render_template

@app.route('/')
def index():
    
    return render_template('index.html', title='Strona Główna')
