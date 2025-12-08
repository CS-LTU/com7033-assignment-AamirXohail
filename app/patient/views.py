from bson.objectid import ObjectId
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required

from . import patient_bp
from .forms import PatientForm
from ..db_mongo import get_mongo_db


def _get_patient_collection():
    db = get_mongo_db()
    return db["patients"]


@patient_bp.route("/", methods=["GET"])
@login_required
def list_patients():
    coll = _get_patient_collection()
    search_id = request.args.get("q", "").strip()

    query = {}
    if search_id:
        query["patient_id"] = search_id

    patients = list(coll.find(query).sort("age", 1))

    return render_template("patient/list.html", patients=patients, search_query=search_id)


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
        coll.delete_one({"_id": ObjectId(patient_id)})
        flash("Patient record deleted.", "info")
    except Exception:
        flash("Could not delete patient.", "danger")

    return redirect(url_for("patient.list_patients"))
