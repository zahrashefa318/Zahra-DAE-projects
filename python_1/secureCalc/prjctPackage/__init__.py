import logging
from flask import Flask 
from .auth import authRouts
from .views import views
from .dbExtension import db
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def flaskApp():
    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'ABCD123'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///userinfo.db'
    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise       
    finally:
        logger.info("Database setup attempt completed.")

    try:
        app.register_blueprint(views)
        app.register_blueprint(authRouts )
        logger.info("Blueprints registered successfully.")
    except Exception as e:
        logger.error(f"Blueprint registration error: {e}")
        raise 
    finally:
        logger.info("Blueprint registration attempt completed.")   
    return app
