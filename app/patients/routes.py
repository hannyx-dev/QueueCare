
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db

patient = Blueprint("patient", __name__)


@patient.route("/dashboard")
@login_required
def dashboard():
    return render_template("patient_dashboard.html", user=current_user)


@patient.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        contact = request.form.get("contact", "").strip()

        if not full_name:
            flash("Full name is required.", "error")
            return redirect(url_for("patient.profile"))

        if len(full_name) > 100:
            flash("Full name cannot exceed 100 characters.", "error")
            return redirect(url_for("patient.profile"))

        if len(contact) > 20:
            flash("Contact number cannot exceed 20 characters.", "error")
            return redirect(url_for("patient.profile"))

        current_user.full_name = full_name
        current_user.contact = contact if contact else None

        db.session.commit()

        flash("Your profile has been updated successfully.", "success")
        return redirect(url_for("patient.profile"))

    return render_template("patient/profile.html", user=current_user)
