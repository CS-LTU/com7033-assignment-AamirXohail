from flask import render_template
from flask_login import login_required

from . import patient_bp


@patient_bp.route("/")
@login_required
def list_patients():
    # Placeholder template
    return render_template("patient/list.html")
