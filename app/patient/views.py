from bson.objectid import ObjectId
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.db_mongo import get_patient_collection, log_activity
from . import patient_bp
from .forms import PatientForm


def _get_patient_collection():
    """
    Thin wrapper so we can change Mongo wiring in one place if needed.
    """
    return get_patient_collection()


@patient_bp.route("/", methods=["GET"])
@login_required
def list_patients():
    coll = _get_patient_collection()
    search_id = request.args.get("q", "").strip()

    query = {}
    if search_id:
        query["patient_id"] = search_id

    patients = list(coll.find(query).sort("age", 1))

    return render_template(
        "patient/list.html",
        patients=patients,
        search_query=search_id,
    )


@patient_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        coll = _get_patient_collection()

        doc = {
            "patient_id": form.patient_id.data or None,
            "gender": form.gender.data,
            "age": form.age.data,
            "hypertension": int(form.hypertension.data),
            "heart_disease": int(form.heart_disease.data),
            "ever_married": form.ever_married.data,
            "work_type": form.work_type.data,
            "residence_type": form.residence_type.data,
            "avg_glucose_level": form.avg_glucose_level.data,
            "bmi": form.bmi.data,
            "smoking_status": form.smoking_status.data,
            "stroke": int(form.stroke.data),
        }

        coll.insert_one(doc)

        # Activity log for patient creation (no raw _id)
        display_id = doc.get("patient_id") or "not specified"
        log_activity(
            username=current_user.username,
            action="CREATE_PATIENT",
            details=f"Created new patient record (hospital id={display_id}).",
        )

        flash("Patient record added.", "success")
        return redirect(url_for("patient.list_patients"))

    return render_template("patient/form.html", form=form, title="Add patient")


@patient_bp.route("/<string:patient_id>/edit", methods=["GET", "POST"])
@login_required
def edit_patient(patient_id):
    coll = _get_patient_collection()
    try:
        patient = coll.find_one({"_id": ObjectId(patient_id)})
    except Exception:
        flash("Invalid patient identifier.", "danger")
        return redirect(url_for("patient.list_patients"))

    if patient is None:
        flash("Patient not found.", "warning")
        return redirect(url_for("patient.list_patients"))

    form = PatientForm(obj=patient)

    # Convert numeric fields to strings for SelectField
    if request.method == "GET":
        form.hypertension.data = str(patient.get("hypertension", 0))
        form.heart_disease.data = str(patient.get("heart_disease", 0))
        form.stroke.data = str(patient.get("stroke", 0))

    if form.validate_on_submit():
        update_doc = {
            "patient_id": form.patient_id.data or None,
            "gender": form.gender.data,
            "age": form.age.data,
            "hypertension": int(form.hypertension.data),
            "heart_disease": int(form.heart_disease.data),
            "ever_married": form.ever_married.data,
            "work_type": form.work_type.data,
            "residence_type": form.residence_type.data,
            "avg_glucose_level": form.avg_glucose_level.data,
            "bmi": form.bmi.data,
            "smoking_status": form.smoking_status.data,
            "stroke": int(form.stroke.data),
        }

        coll.update_one({"_id": ObjectId(patient_id)}, {"$set": update_doc})

        # Use the edited hospital id for a clean log message
        display_id = update_doc.get("patient_id") or "not specified"
        log_activity(
            username=current_user.username,
            action="UPDATE_PATIENT",
            details=f"Updated patient record (hospital id={display_id}).",
        )

        flash("Patient record updated.", "success")
        return redirect(url_for("patient.list_patients"))

    return render_template("patient/form.html", form=form, title="Edit patient")


@patient_bp.route("/<string:patient_id>/view", methods=["GET"])
@login_required
def view_patient(patient_id):
    coll = _get_patient_collection()
    try:
        patient = coll.find_one({"_id": ObjectId(patient_id)})
    except Exception:
        flash("Invalid patient identifier.", "danger")
        return redirect(url_for("patient.list_patients"))

    if patient is None:
        flash("Patient not found.", "warning")
        return redirect(url_for("patient.list_patients"))

    return render_template("patient/detail.html", patient=patient)


@patient_bp.route("/<string:patient_id>/delete", methods=["POST"])
@login_required
def delete_patient(patient_id):
    coll = _get_patient_collection()
    try:
        # Fetch once so we can get the friendly hospital id
        doc = coll.find_one({"_id": ObjectId(patient_id)})
        coll.delete_one({"_id": ObjectId(patient_id)})

        display_id = (doc or {}).get("patient_id") or "not specified"
        log_activity(
            username=current_user.username,
            action="DELETE_PATIENT",
            details=f"Deleted patient record (hospital id={display_id}).",
        )

        flash("Patient record deleted.", "info")
    except Exception:
        flash("Could not delete patient.", "danger")

    return redirect(url_for("patient.list_patients"))
