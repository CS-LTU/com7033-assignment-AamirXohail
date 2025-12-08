from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Optional


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=120),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=128),
        ],
    )
    submit = SubmitField("Sign in")


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=120),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=128),
        ],
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Create account")



class ProfileForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=64),
        ],
    )
    current_password = PasswordField(
        "Current password",
        validators=[DataRequired()],
    )
    new_password = PasswordField(
        "New password",
        validators=[
            Optional(),
            Length(min=8, message="New password should be at least 8 characters."),
        ],
    )
    confirm_new_password = PasswordField(
        "Confirm new password",
        validators=[
            Optional(),
            EqualTo("new_password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Save changes")