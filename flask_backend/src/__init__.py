# Some set up for the application 

from flask import Flask


def create_app():
    app = Flask(__name__)
    
    # Add a default route
    @app.route("/")
    def welcome():
        return "<h1>PLAY PIANO</h1>"

    # Import the various routes
    from src.keys import keys
    # from src.metadata import metadata
    from src.session_info import session_info

    # Register the routes that we just imported so they can be properly handled
    app.register_blueprint(keys, url_prefix='/k')
    # app.register_blueprint(metadata, url_prefix='/md')
    app.register_blueprint(session_info, url_prefix='/si')

    return app