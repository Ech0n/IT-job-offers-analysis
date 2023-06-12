from app import app
from flask.templating import render_template

from app import charts
import os 

@app.route('/github_chart')
def chart_github_popularity():

    graphJSON = charts.github_bubble_chart(os.path.join(app.config['UPLOAD_FOLDER'], 'github_data29_05_2023.csv'))
    return render_template('chart_example.html', graphJSON = graphJSON)