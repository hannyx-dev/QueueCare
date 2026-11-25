
from flask import Blueprint, render_template
from flask_login import login_required, current_user

patient = Blueprint("patient", __name__)


@patient.route("/dashboard")
@login_required
def dashboard():
    return render_template("patient_dashboard.html", user=current_user)
