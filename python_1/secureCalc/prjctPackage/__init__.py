import logging
from flask import Flask 
from .auth import authRouts
from .views import views
from .dbExtension import db
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def flaskApp():
     """
    Initializes and configures a Flask application instance.

    This function performs the following operations:
    1. Creates a Flask application.
    2. Configures the application with a secret key and a SQLite database URI.
    3. Initializes the SQLAlchemy database extension and creates all database tables within the application context.
    4. Registers the provided blueprints for views and authentication routes.
    5. Implements logging to record the success or failure of database initialization and blueprint registration.

    Returns:
        Flask: The configured Flask application instance.

    Raises:
        Exception: Propagates any exceptions encountered during database initialization or blueprint registration.
    """
    
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
