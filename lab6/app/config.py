import os

SECRET_KEY = 'secret-key'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:mospolytech@127.0.0.1/lab6'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    '..',
    'media', 
    'images'
)
