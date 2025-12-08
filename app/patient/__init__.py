from flask import Blueprint

patient_bp = Blueprint("patient", __name__, url_prefix="/patients")

from . import views  # noqa: E402,F401
