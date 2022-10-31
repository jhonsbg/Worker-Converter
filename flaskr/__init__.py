from flask import Flask

def create_app(config_name):
    app = Flask(__name__)

    app.config['UPLOADS_FOLDER'] = 'uploads/audios/2/'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/osboxes/Proyecto_cloud/instance/tutorial_canciones.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://andescloud:123456@34.72.155.184:5432/andescloud'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   

    return app