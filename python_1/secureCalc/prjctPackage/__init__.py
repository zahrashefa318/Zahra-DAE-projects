from flask import Flask 
from .auth import authRouts
from .simpleArithmetic import SimpleArithmetic
from .dbExtension import db

def flaskApp():
    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'ABCD123'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///userinfo.db'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    obj=SimpleArithmetic()
    
    
    app.register_blueprint(authRouts )
    return app
