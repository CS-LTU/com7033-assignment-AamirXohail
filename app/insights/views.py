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


@insights_bp.route("/data-overview")
@login_required
def data_overview():
    """
    Data quality and structure overview for the stroke dataset.
    """
    df = _load_stroke_data()
    if df is None:
        return render_template(
            "insights/data_overview.html",
            data_available=False,
            dataset_path=current_app.config["STROKE_DATA_PATH"],
        )

    # Preview top rows
    preview_html = (
        df.head(10)
        .to_html(classes="table table-sm table-striped mb-0", index=False)
    )

    # Missing values per column
    missing_series = df.isna().sum()
    missing_df = (
        missing_series.reset_index()
        .rename(columns={"index": "Column", 0: "Missing values"})
    )
    missing_html = missing_df.to_html(
        classes="table table-sm table-bordered mb-0", index=False
    )

    # Summary stats for numeric columns
    numeric_df = df.select_dtypes(include=["float64", "int64"])
    if not numeric_df.empty:
        summary_df = numeric_df.describe().T.reset_index().rename(
            columns={"index": "Column"}
        )
        summary_html = summary_df.to_html(
            classes="table table-sm table-striped mb-0", index=False
        )
    else:
        summary_html = None

    # Outlier counts using IQR method
    outlier_rows = []
    for col in numeric_df.columns:
        series = numeric_df[col].dropna()
        if series.empty:
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_count = int(((series < lower) | (series > upper)).sum())
        outlier_rows.append({"Column": col, "Outliers": outlier_count})

    if outlier_rows:
        outlier_df = pd.DataFrame(outlier_rows)
        outlier_html = outlier_df.to_html(
            classes="table table-sm table-hover mb-0", index=False
        )
    else:
        outlier_html = None

    # Simple column descriptions (you can expand later in the report)
    column_descriptions = {
        "id": "Internal row identifier provided with the dataset.",
        "gender": "Recorded biological sex of the patient.",
        "age": "Age in years at the time of data collection.",
        "hypertension": "Indicator for diagnosed high blood pressure (1=yes, 0=no).",
        "heart_disease": "Flag for known heart disease history (1=yes, 0=no).",
        "ever_married": "Whether the patient reports having ever been married.",
        "work_type": "Employment category such as private, self employed or government.",
        "Residence_type": "Patient residence type (urban or rural).",
        "avg_glucose_level": "Mean glucose measurement at the time of collection.",
        "bmi": "Body mass index derived from height and weight where available.",
        "smoking_status": "Simplified smoking history label.",
        "stroke": "Outcome label used as target variable (1=stroke, 0=no stroke).",
    }

    return render_template(
        "insights/data_overview.html",
        data_available=True,
        dataset_path=current_app.config["STROKE_DATA_PATH"],
        preview_html=preview_html,
        missing_html=missing_html,
        summary_html=summary_html,
        outlier_html=outlier_html,
        column_descriptions=column_descriptions,
    )
