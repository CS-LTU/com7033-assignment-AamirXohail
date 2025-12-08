from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    FloatField,
    SelectField,
    SubmitField,
)
from wtforms.validators import DataRequired, Optional, NumberRange, Length


class PatientForm(FlaskForm):
    patient_id = StringField(
        "Patient ID",
        validators=[Optional(), Length(max=50)],
    )

    gender = SelectField(
        "Gender",
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        validators=[DataRequired()],
    )

    age = IntegerField(
        "Age",
        validators=[DataRequired(), NumberRange(min=0, max=120)],
    )

    hypertension = SelectField(
        "Hypertension",
        choices=[("0", "No"), ("1", "Yes")],
        validators=[DataRequired()],
    )

    heart_disease = SelectField(
        "Heart disease",
        choices=[("0", "No"), ("1", "Yes")],
        validators=[DataRequired()],
    )

    ever_married = SelectField(
        "Ever married",
        choices=[("Yes", "Yes"), ("No", "No")],
        validators=[DataRequired()],
    )

    work_type = SelectField(
        "Work type",
        choices=[
            ("Private", "Private"),
            ("Self-employed", "Self-employed"),
            ("Govt_job", "Government job"),
            ("children", "Children"),
            ("Never_worked", "Never worked"),
        ],
        validators=[DataRequired()],
    )

    residence_type = SelectField(
        "Residence type",
        choices=[("Urban", "Urban"), ("Rural", "Rural")],
        validators=[DataRequired()],
    )

    avg_glucose_level = FloatField(
        "Average glucose level",
        validators=[DataRequired(), NumberRange(min=0)],
    )

    bmi = FloatField(
        "BMI",
        validators=[Optional(), NumberRange(min=0)],
    )

    smoking_status = SelectField(
        "Smoking status",
        choices=[
            ("never smoked", "Never smoked"),
            ("formerly smoked", "Formerly smoked"),
            ("smokes", "Smokes"),
            ("Unknown", "Unknown"),
        ],
        validators=[DataRequired()],
    )

    stroke = SelectField(
        "Stroke outcome",
        choices=[("0", "No stroke"), ("1", "Stroke")],
        validators=[DataRequired()],
    )

    submit = SubmitField("Save patient")
