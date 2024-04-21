from flask import Flask
from os import path

def create_app():
    app = Flask(__name__, template_folder='/home/stellapps/Cab_Rental_System/webapp')
    app.secret_key = "aZfretWedf@wRFgtYH"

    from .auth.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    return app