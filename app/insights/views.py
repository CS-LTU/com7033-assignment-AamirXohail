import os
from datetime import datetime

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-GUI backend for servers
import matplotlib.pyplot as plt

from flask import (
    render_template,
    current_app,
    flash,
    request,
)
from flask_login import login_required, current_user
from pymongo.errors import ServerSelectionTimeoutError

from . import insights_bp
from app.db_mongo import get_activity_collection, log_activity

def _load_stroke_data():
    """
    Load the stroke dataset from the configured CSV path.
    Returns a pandas DataFrame or None if the file is missing.
    """
    csv_path = current_app.config["STROKE_DATA_PATH"]
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        return None
    except Exception as exc:
        current_app.logger.warning("Could not read stroke dataset: %s", exc)
        return None
    return df


def _charts_dir():
    """
    Absolute path to the folder where we store generated charts.
    """
    charts_root = os.path.join(current_app.static_folder, "charts")
    os.makedirs(charts_root, exist_ok=True)
    return charts_root


def _save_fig(path: str):
    """
    Helper to save the current matplotlib figure and close it.
    """
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()


def _generate_summary_charts(df: pd.DataFrame) -> dict:
    """
    Generate core summary charts and return mapping of chart keys to
    static file paths (relative to the 'static' folder).
    """
    charts_root = _charts_dir()

    gender_file = "charts/gender_distribution.png"
    stroke_file = "charts/stroke_distribution.png"
    age_file = "charts/age_histogram.png"
    bmi_file = "charts/bmi_histogram.png"
    heatmap_file = "charts/correlation_heatmap.png"

    # 1. Gender distribution (horizontal bar)
    if "gender" in df.columns:
        plt.figure(figsize=(4.5, 3.5))
        df["gender"].value_counts().plot(kind="barh")
        plt.title("Gender distribution")
        plt.xlabel("Count")
        plt.ylabel("Gender")
        _save_fig(os.path.join(charts_root, "gender_distribution.png"))

    # 2. Stroke vs no stroke
    if "stroke" in df.columns:
        plt.figure(figsize=(4.5, 3.5))
        df["stroke"].value_counts().rename({0: "No stroke", 1: "Stroke"}).plot(
            kind="bar"
        )
        plt.title("Stroke vs no stroke")
        plt.xlabel("Outcome")
        plt.ylabel("Count")
        _save_fig(os.path.join(charts_root, "stroke_distribution.png"))

    # 3. Age distribution
    if "age" in df.columns:
        plt.figure(figsize=(5, 3.5))
        df["age"].dropna().plot(kind="hist", bins=20)
        plt.title("Age distribution")
        plt.xlabel("Age (years)")
        plt.ylabel("Number of patients")
        _save_fig(os.path.join(charts_root, "age_histogram.png"))

    # 4. BMI distribution
    if "bmi" in df.columns:
        plt.figure(figsize=(5, 3.5))
        df["bmi"].dropna().plot(kind="hist", bins=20)
        plt.title("BMI distribution")
        plt.xlabel("BMI")
        plt.ylabel("Number of patients")
        _save_fig(os.path.join(charts_root, "bmi_histogram.png"))

    # 5. Correlation heatmap
    numeric_df = df.select_dtypes(include=["float64", "int64"])
    if not numeric_df.empty:
        corr = numeric_df.corr()
        plt.figure(figsize=(6, 4.5))
        im = plt.imshow(corr, aspect="auto")
        plt.colorbar(im, fraction=0.046, pad=0.04)
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
        plt.yticks(range(len(corr.columns)), corr.columns)
        plt.title("Correlation heatmap")
        _save_fig(os.path.join(charts_root, "correlation_heatmap.png"))

    return {
        "gender": gender_file,
        "stroke": stroke_file,
        "age": age_file,
        "bmi": bmi_file,
        "heatmap": heatmap_file,
    }


def _load_stroke_data():
    """
    Load the stroke dataset from the configured CSV path.
    Returns a pandas DataFrame or None if the file is missing.
    """
    csv_path = current_app.config["STROKE_DATA_PATH"]
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        return None
    except Exception as exc:  # pragma: no cover
        current_app.logger.warning("Could not read stroke dataset: %s", exc)
        return None
    return df


def _charts_dir():
    """
    Absolute path to the folder where we store generated charts.
    """
    charts_root = os.path.join(current_app.static_folder, "charts")
    os.makedirs(charts_root, exist_ok=True)
    return charts_root


def _save_fig(path: str):
    """
    Helper to save the current matplotlib figure and close it.
    """
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()


def _generate_summary_charts(df: pd.DataFrame) -> dict:
    """
    Generate core summary charts and return mapping of chart keys to
    static file paths (relative to the 'static' folder).
    """
    charts_root = _charts_dir()

    gender_file = "charts/gender_distribution.png"
    stroke_file = "charts/stroke_distribution.png"
    age_file = "charts/age_histogram.png"
    bmi_file = "charts/bmi_histogram.png"
    heatmap_file = "charts/correlation_heatmap.png"

    # 1. Gender distribution
    if "gender" in df.columns:
        plt.figure(figsize=(4, 4))
        df["gender"].value_counts().plot(kind="bar")
        plt.title("Gender distribution")
        plt.xlabel("Gender")
        plt.ylabel("Count")
        _save_fig(os.path.join(charts_root, "gender_distribution.png"))

    # 2. Stroke vs no-stroke
    if "stroke" in df.columns:
        plt.figure(figsize=(4, 4))
        df["stroke"].value_counts().rename({0: "No stroke", 1: "Stroke"}).plot(
            kind="bar"
        )
        plt.title("Stroke vs no-stroke")
        plt.xlabel("Outcome")
        plt.ylabel("Count")
        _save_fig(os.path.join(charts_root, "stroke_distribution.png"))

    # 3. Age distribution
    if "age" in df.columns:
        plt.figure(figsize=(5, 4))
        df["age"].dropna().plot(kind="hist", bins=20)
        plt.title("Age distribution")
        plt.xlabel("Age (years)")
        plt.ylabel("Number of patients")
        _save_fig(os.path.join(charts_root, "age_histogram.png"))

    # 4. BMI distribution
    if "bmi" in df.columns:
        plt.figure(figsize=(5, 4))
        df["bmi"].dropna().plot(kind="hist", bins=20)
        plt.title("BMI distribution")
        plt.xlabel("BMI")
        plt.ylabel("Number of patients")
        _save_fig(os.path.join(charts_root, "bmi_histogram.png"))

    # 5. Correlation heatmap for numeric columns
    numeric_df = df.select_dtypes(include=["float64", "int64"])
    if not numeric_df.empty:
        corr = numeric_df.corr()
        plt.figure(figsize=(6, 5))
        im = plt.imshow(corr, aspect="auto")
        plt.colorbar(im, fraction=0.046, pad=0.04)
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
        plt.yticks(range(len(corr.columns)), corr.columns)
        plt.title("Correlation heatmap (numeric features)")
        _save_fig(os.path.join(charts_root, "correlation_heatmap.png"))

    return {
        "gender": gender_file,
        "stroke": stroke_file,
        "age": age_file,
        "bmi": bmi_file,
        "heatmap": heatmap_file,
    }


@insights_bp.route("/dashboard")
@login_required
def dashboard():
    """
    Main landing page once authenticated.
    Shows high level KPIs and visual charts for the stroke dataset.
    """
    df = _load_stroke_data()
    dataset_path = current_app.config["STROKE_DATA_PATH"]

    if df is None:
        return render_template(
            "insights/dashboard.html",
            data_available=False,
            dataset_path=dataset_path,
        )

    total_records = len(df)
    avg_age = round(df["age"].mean(), 1) if "age" in df.columns else None
    avg_bmi = round(df["bmi"].mean(), 1) if "bmi" in df.columns else None
    if "stroke" in df.columns:
        stroke_rate = round(df["stroke"].mean() * 100, 2)
    else:
        stroke_rate = None

    chart_files = _generate_summary_charts(df)

    return render_template(
        "insights/dashboard.html",
        data_available=True,
        dataset_path=dataset_path,
        total_patients=total_records,
        avg_age=avg_age,
        avg_bmi=avg_bmi,
        stroke_rate=stroke_rate,
        gender_img=chart_files["gender"],
        stroke_img=chart_files["stroke"],
        age_img=chart_files["age"],
        bmi_img=chart_files["bmi"],
        heatmap_img=chart_files["heatmap"],
    )


@insights_bp.route("/data-overview")
@login_required
def data_overview():
    """
    Data quality and structure overview for the stroke dataset.
    """
    df = _load_stroke_data()
    dataset_path = current_app.config["STROKE_DATA_PATH"]

    if df is None:
        return render_template(
            "insights/data_overview.html",
            data_available=False,
            dataset_path=dataset_path,
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
        dataset_path=dataset_path,
        preview_html=preview_html,
        missing_html=missing_html,
        summary_html=summary_html,
        outlier_html=outlier_html,
        column_descriptions=column_descriptions,
    )


@insights_bp.route("/activity-log")
@login_required
def activity_log():
    """
    Read the latest activity entries from MongoDB and render them in a table.
    """
    coll = get_activity_collection()
    try:
        docs = list(coll.find().sort("timestamp", -1).limit(100))
    except ServerSelectionTimeoutError:
        docs = []
        flash(
            "Could not connect to the activity log store. "
            "Please verify MongoDB configuration.",
            "danger",
        )

    logs = []
    for d in docs:
        logs.append(
            {
                "username": d.get("username", "unknown"),
                "action": d.get("action", "UNKNOWN"),
                "details": d.get("details") or "",
                "timestamp": d.get("timestamp"),
            }
        )

    return render_template("insights/activity_log.html", logs=logs)


@insights_bp.route("/data-upload", methods=["GET", "POST"])
@login_required
def data_upload():
    """
    Allow an authenticated user to upload/replace the stroke dataset CSV.
    The file is stored at the configured STROKE_DATA_PATH and used
    by the dashboard and data overview pages.
    """
    preview_html = None
    dataset_path = current_app.config["STROKE_DATA_PATH"]

    if request.method == "POST":
        file = request.files.get("csv_file")
        if not file or file.filename == "":
            flash("Please choose a CSV file to upload.", "warning")
        elif not file.filename.lower().endswith(".csv"):
            flash("Only CSV files are accepted.", "warning")
        else:
            # Ensure folder exists
            os.makedirs(os.path.dirname(dataset_path), exist_ok=True)

            # Save file as the configured dataset file
            file.save(dataset_path)

            log_activity(
                username=current_user.username,
                action="UPLOAD_DATASET",
                details=f"Uploaded new stroke dataset ({os.path.basename(dataset_path)}).",
            )

            flash(
                "Dataset uploaded successfully. Analytics will now use the new file.",
                "success",
            )

            # Try to show a small preview
            try:
                df = pd.read_csv(dataset_path)
                preview_html = df.head(10).to_html(
                    classes="table table-sm table-striped mb-0", index=False
                )
            except Exception:
                preview_html = None
                flash(
                    "File was saved but could not be parsed as CSV. "
                    "Please verify the file structure.",
                    "danger",
                )

    return render_template(
        "insights/data_upload.html",
        preview=preview_html,
        dataset_path=dataset_path,
    )


@insights_bp.route("/data-visuals")
@login_required
def data_visuals():
    """
    Dedicated page for visual summaries of the stroke dataset.
    Dashboard stays lightweight; this page hosts the charts.
    """
    df = _load_stroke_data()
    if df is None:
        flash(
            "No dataset found. Please upload a CSV file first.",
            "warning",
        )
        return redirect(url_for("insights.data_overview"))

    total_records = len(df)
    avg_age = round(df["age"].mean(), 1) if "age" in df.columns else None
    avg_bmi = round(df["bmi"].mean(), 1) if "bmi" in df.columns else None
    stroke_rate = (
        round(df["stroke"].mean() * 100, 2)
        if "stroke" in df.columns
        else None
    )

    chart_files = _generate_summary_charts(df)

    return render_template(
        "insights/data_visuals.html",
        total_patients=total_records,
        avg_age=avg_age,
        avg_bmi=avg_bmi,
        stroke_rate=stroke_rate,
        gender_img=chart_files["gender"],
        stroke_img=chart_files["stroke"],
        age_img=chart_files["age"],
        bmi_img=chart_files["bmi"],
        heatmap_img=chart_files["heatmap"],
    )
