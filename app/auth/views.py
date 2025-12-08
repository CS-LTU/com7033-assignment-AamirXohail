from flask import render_template, redirect, url_for, flash, request
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)

from app.extensions import db
from app.models import AppUser
from . import auth_bp
from .forms import LoginForm, RegisterForm, ProfileForm


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("insights.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = AppUser.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.", "danger")
            return render_template("auth/login.html", form=form)

        login_user(user, remember=False)
        flash("You have signed in successfully.", "success")
        next_page = request.args.get("next") or url_for("insights.dashboard")
        return redirect(next_page)

    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("insights.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        existing = AppUser.query.filter_by(username=form.username.data).first()
        if existing:
            flash("That username is already registered.", "warning")
            return render_template("auth/register.html", form=form)

        user = AppUser(username=form.username.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """
    Allow the currently authenticated user to update their username and password.
    """
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        # 1. Verify current password
        if not current_user.check_password(form.current_password.data):
            flash("Current password is incorrect.", "danger")
            return render_template("auth/profile.html", form=form)

        # 2. If username changed, check for uniqueness
        if form.username.data != current_user.username:
            existing = AppUser.query.filter_by(username=form.username.data).first()
            if existing and existing.id != current_user.id:
                flash("That username is already taken.", "warning")
                return render_template("auth/profile.html", form=form)
            current_user.username = form.username.data

        # 3. If new password provided, update it
        if form.new_password.data:
            current_user.set_password(form.new_password.data)

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("auth.profile"))

    return render_template("auth/profile.html", form=form)
