from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User
from forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(
            url_for("admin.admin_dashboard" if current_user.is_admin() else "user.user_dashboard")
        )

    form = LoginForm()
    if form.validate_on_submit():
        print(f"DEBUG: Form submitted with email: {form.email.data}")
        user = User.query.filter_by(email=form.email.data.lower()).first()
        print(f"DEBUG: User found: {user}")
        if user:
            print(f"DEBUG: User email: {user.email}, role: {user.role}")
        if not user or not check_password_hash(user.password_hash, form.password.data):
            print("DEBUG: Invalid email or password")
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)
        flash("Logged in successfully", "success")
        return redirect(
            url_for("admin.admin_dashboard" if user.is_admin() else "user.user_dashboard")
        )

    return render_template("login.html", form=form)



@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("user.user_dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data.lower()).first()
        if existing:
            flash("Email already registered", "warning")
            return redirect(url_for("auth.register"))

        user = User(
            full_name=form.full_name.data,
            email=form.email.data.lower(),
            phone=form.phone.data,
            password_hash=generate_password_hash(form.password.data),
            aadhaar_number=form.aadhaar_number.data,
            pan_number=form.pan_number.data,
            address=form.address.data,
            bank_account_number=form.bank_account_number.data,
            ifsc_code=form.ifsc_code.data,
            role="USER",
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))
