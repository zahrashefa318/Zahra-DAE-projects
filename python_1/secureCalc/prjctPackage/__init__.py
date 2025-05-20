from flask import Flask 
from .auth import authRouts
from .views import views
from .dbExtension import db

def flaskApp():
    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'ABCD123'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///userinfo.db'
    db.init_app(app)
    with app.app_context():
        db.create_all()

    
    app.register_blueprint(views)
    app.register_blueprint(authRouts )
    return app
