from flask import Blueprint

insights_bp = Blueprint("insights", __name__, url_prefix="/insights")

from . import views  # noqa: E402,F401
