from flask import render_template, request, redirect, url_for
from sqlalchemy import func
from pythondb import pythondb_bp
from models import db, Users, Emails, PhoneNumbers


# connects default URL to a function
@pythondb_bp.route('/')
def databases():
    """convert Users table into a list of dictionary rows"""
    records = []
    users = Users.query.all()
    for user in users:
        user_dict = {'id': user.UserID, 'name': user.username, 'password': user.password}
        # filter email
        email = Emails.query.filter_by(UserID=user.UserID).first()
        if email:
            user_dict['emails'] = email.email_address
        # filter phone number
        pn = PhoneNumbers.query.filter_by(UserID=user.UserID).first()
        if pn:
            user_dict['phone_numbers'] = pn.phone_number
        # append to records
        records.append(user_dict)
    return render_template("pythondb/index.html", table=records)


# create/add a new record to the table
@pythondb_bp.route('/create/', methods=["POST"])
def create():
    if request.form:
        """prepare data for primary table extracting from form"""
        user = Users(username=request.form.get("username"), password=request.form.get("password"))
        """add and commit data to user table"""
        db.session.add(user)
        db.session.commit()
        """prepare data for related tables extracting from form and using new UserID """
        userid = db.session.query(func.max(Users.UserID))
        email = Emails(email_address=request.form.get("email"), UserID=userid)
        phone_number = PhoneNumbers(phone_number=request.form.get("phone_number"), UserID=userid)
        """email table add and commit"""
        db.session.add(email)
        db.session.commit()
        """phone number table add and commit"""
        db.session.add(phone_number)
        db.session.commit()
    return redirect(url_for('pythondb_bp.databases'))



# CRUD delete
@pythondb_bp.route('/delete/', methods=["POST"])
def delete():
    if request.form:
        """fetch userid"""
        userid = request.form.get("ID")
        """delete userid rows from emails table"""
        db.session.query(Emails).filter(Emails.UserID == userid).delete()
        """delete userid rows from phone numbers table"""
        db.session.query(PhoneNumbers).filter(PhoneNumbers.UserID == userid).delete()
        """delete userid rows from users table"""
        db.session.query(Users).filter(Users.UserID == userid).delete()
        """commit changes to database"""
        db.session.commit()
    return redirect(url_for('pythondb_bp.databases'))


# if email url, show the email table only
@pythondb_bp.route('/emails/')
def emails():
    # fill the table with emails only
    records = []
    emails = Emails.query.all()
    for email in emails:
        user_dict = {}
        user_dict['id'] = email.UserID
        user_dict['emails'] = email.email_address
        records.append(user_dict)
    return render_template("pythondb/index.html", table=records)


# if phones url, show phones table only
@pythondb_bp.route('/phones/')
def phones():
    # fill the table with phone numbers only
    records = []
    phone_numbers = PhoneNumbers.query.all()
    for phone in phone_numbers:
        user_dict = {}
        user_dict['id'] = phone.UserID
        user_dict['phone_numbers'] = phone.phone_number
        records.append(user_dict)
    return render_template("pythondb/index.html", table=records)

