# Some set up for the application 

from flask import Flask


def create_app():
    app = Flask(__name__)
    
    # Add a default route
    @app.route("/")
    def welcome():
        return "<h1>PLAY PIANO</h1>"

    # Import the various routes
    from src.key_input import key_input
    from src.conductor import conductor

    # Register the routes that we just imported so they can be properly handled
    app.register_blueprint(key_input, url_prefix='/keyinput')
    app.register_blueprint(conductor, url_prefix='/conductor')

    return app