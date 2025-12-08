from flask import Flask, render_template
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

    # Login settings
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # Register blueprints
    from .auth import auth_bp
    from .patient import patient_bp
    from .insights import insights_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(insights_bp)

    # Home route
    @app.route("/")
    def home():
        return render_template("insights/dashboard.html")

    # Ensure Mongo client is closed after each app context
    app.teardown_appcontext(close_mongo_client)

    # Create SQL tables (users) on first run
    with app.app_context():
        db.create_all()

    return app
