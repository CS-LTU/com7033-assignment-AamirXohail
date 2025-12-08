import pandas as pd
from flask import render_template, current_app
from flask_login import login_required

from . import insights_bp


def _load_stroke_data():
    csv_path = current_app.config["STROKE_DATA_PATH"]
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        return None
    return df


@insights_bp.route("/dashboard")
@login_required
def dashboard():
    df = _load_stroke_data()

    if df is None:
        return render_template(
            "insights/dashboard.html",
            total_records=0,
            avg_age=None,
            avg_bmi=None,
            stroke_rate=None,
            data_available=False,
        )

    total_records = len(df)
    avg_age = round(df["age"].mean(), 1) if "age" in df.columns else None
    avg_bmi = round(df["bmi"].mean(), 1) if "bmi" in df.columns else None

    if "stroke" in df.columns:
        stroke_rate = round(df["stroke"].mean() * 100, 2)
    else:
        stroke_rate = None

    return render_template(
        "insights/dashboard.html",
        total_records=total_records,
        avg_age=avg_age,
        avg_bmi=avg_bmi,
        stroke_rate=stroke_rate,
        data_available=True,
    )
