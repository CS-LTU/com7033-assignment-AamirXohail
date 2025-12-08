from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from . import auth_bp
from ..extensions import db
from ..models import AppUser


@auth_bp.route("/login")
def login():
    # Temporary simple page; will replace with Flask-WTF form
    return render_template("auth/login.html")


@auth_bp.route("/register")
def register():
    # Temporary simple page; will replace with Flask-WTF form
    return render_template("auth/register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
