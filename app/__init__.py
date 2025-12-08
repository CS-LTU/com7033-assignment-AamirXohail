from flask import Flask, redirect, url_for
from flask_login import current_user

from config import config_map
from .extensions import db, login_manager, csrf
from .db_mongo import close_mongo_client


def create_hospital_app(config_name: str = "default") -> Flask:
    """
    Application factory for the Hospital Management system.
    """
    app = Flask(__name__)

    # Load configuration from root config.py
    config_class = config_map.get(config_name, config_map["default"])
    app.config.from_object(config_class)

    # Initialise extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Login manager configuration
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # Register blueprints
    from .auth import auth_bp
    from .patient import patient_bp
    from .insights import insights_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(insights_bp)

    # Home route: redirect depending on auth status
    @app.route("/")
    def home():
        if current_user.is_authenticated:
            return redirect(url_for("insights.dashboard"))
        return redirect(url_for("auth.login"))

    # Close Mongo client at the end of the app context
    app.teardown_appcontext(close_mongo_client)

    # Create SQL tables (for users etc.) on first run
    with app.app_context():
        db.create_all()

    return app
