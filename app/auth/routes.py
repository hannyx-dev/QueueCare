
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        contact = request.form.get("contact", "").strip()

        if not full_name or not email or not password:
            flash("Please complete all required fields.", "error")
            return redirect(url_for("auth.register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "error")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("An account with this email already exists.", "error")
            return redirect(url_for("auth.register"))

        user = User(
            full_name=full_name,
            email=email,
            role="patient",
            contact=contact if contact else None
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("patient.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password) and user.is_active:
            if user.role != "patient":
                flash("Please use the appropriate login for your account.", "error")
                return redirect(url_for("auth.login"))

            login_user(user)
            return redirect(url_for("patient.dashboard"))

        flash("Invalid email or password.", "error")
        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
