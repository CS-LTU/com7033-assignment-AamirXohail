from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from . import auth_bp
from .forms import LoginForm, RegisterForm
from ..extensions import db
from ..models import AppUser


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("insights.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        existing = AppUser.query.filter_by(username=form.username.data.strip()).first()
        if existing:
            flash("This username is already taken. Please choose another one.", "danger")
            return render_template("auth/register.html", form=form)

        user = AppUser(username=form.username.data.strip())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("insights.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = AppUser.query.filter_by(username=form.username.data.strip()).first()
        if user is None or not user.verify_password(form.password.data):
            flash("Invalid username or password.", "danger")
            return render_template("auth/login.html", form=form)

        login_user(user)
        flash("Welcome back, {}!".format(user.username), "success")

        next_page = request.args.get("next")
        return redirect(next_page or url_for("insights.dashboard"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
