from flask import Flask

def create_app(): 
    app = Flask(__name__)

    # Set config
    app.config.from_object('config.Config')
    
    return app


app = create_app()

from app import views, chart_views
