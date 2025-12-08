from flask import render_template
from flask_login import login_required

from . import insights_bp


@insights_bp.route("/dashboard")
@login_required
def dashboard():
    # Placeholder analytics dashboard
    return render_template("insights/dashboard.html")
