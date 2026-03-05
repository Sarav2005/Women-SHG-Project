from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    FloatField,
    BooleanField,
    DateField,
    SelectField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[Optional(), Length(max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    aadhaar_number = StringField("Aadhaar Number", validators=[Optional(), Length(max=12)])
    pan_number = StringField("PAN Number", validators=[Optional(), Length(max=10)])
    address = TextAreaField("Address", validators=[Optional(), Length(max=255)])
    bank_account_number = StringField("Bank Account Number", validators=[Optional()])
    ifsc_code = StringField("IFSC Code", validators=[Optional(), Length(max=20)])
    submit = SubmitField("Register")


class SavingsForm(FlaskForm):
    month = StringField("Month", validators=[DataRequired()])
    amount = FloatField("Amount", validators=[DataRequired()])
    payment_date = DateField("Payment Date", default=date.today, validators=[DataRequired()])
    submit = SubmitField("Add Savings")


class LoanApplyForm(FlaskForm):
    loan_amount = FloatField("Loan Amount", validators=[DataRequired()])
    interest_rate = FloatField("Interest Rate (%)", validators=[DataRequired()])
    issue_date = DateField("Issue Date", default=date.today, validators=[DataRequired()])
    due_date = DateField("Due Date", validators=[DataRequired()])
    submit = SubmitField("Apply Loan")


class AttendanceForm(FlaskForm):
    meeting_date = DateField("Meeting Date", default=date.today, validators=[DataRequired()])
    present = BooleanField("Present", default=True)
    submit = SubmitField("Mark Attendance")


class ApproveLoanForm(FlaskForm):
    status = SelectField(
        "Status",
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Paid", "Paid")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Update Loan")


class SimpleSearchForm(FlaskForm):
    query = StringField("Search", validators=[Optional()])
    submit = SubmitField("Search")
