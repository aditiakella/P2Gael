from app import app
import dataaboutus
import requests
from flask import render_template, request, redirect, url_for
from models.crud import model_create, model_delete, model_query_all, model_query_emails, \
    model_query_phones


# connects default URL to a function
@app.route('/database/')
def databases():
    """convert Users table into a list of dictionary rows"""
    records = model_query_all()
    return render_template("index.html", table=records)


# create/add a new record to the table
@app.route('/create/', methods=["POST"])
def create():
    if request.form:
        """extract data from form"""
        user_dict = {'username': request.form.get("username"), 'password': request.form.get("password"),
                     'email': request.form.get("email"), 'phone_number': request.form.get("phone_number")}
        # model_create expects: username, password, email, phone_number
        model_create(user_dict)
    return redirect(url_for('.databases'))


# CRUD delete
@app.route('/delete/', methods=["POST"])
def delete():
    if request.form:
        """fetch userid"""
        userid = request.form.get("ID")
        model_delete(userid)
    return redirect(url_for('.databases'))


# if email url, show the email table only
@app.route('/emails/')
def emails():
    # fill the table with emails only
    records = model_query_emails()
    return render_template("index.html", table=records)


# if phones url, show phones table only
@app.route('/phones/')
def phones():
    # fill the table with phone numbers only
    records = model_query_phones()
    return render_template("index.html", table=records)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/base/')
def index():
    return render_template("base.html")


@app.route('/aboutus/')
def about():
    print("About us")
    #Flask import uses Jinga to render HTML
    return render_template("About.html", data=dataaboutus.alldata())

@app.route('/aboutus/aditi/')
def aditi():
    #Flask import uses Jinga to render HTML
    return render_template("aditi.html", data=dataaboutus.aditis_info())
@app.route('/aboutus/sophie/')
def sophie():
    #Flask import uses Jinga to render HTML
    return render_template("sophie.html", data=dataaboutus.sophies_info())
@app.route('/aboutus/grace/')
def grace():
    #Flask import uses Jinga to render HTML
    return render_template("grace.html", data=dataaboutus.graces_info())
@app.route('/aboutus/luke/')
def luke():
    #Flask import uses Jinga to render HTML
    return render_template("luke.html", data=dataaboutus.lukes_info())

@app.route('/Phylogenetic/')
def Phylogenetic():
    return render_template("Phylogenetic.html")

@app.route('/twitter', methods=['GET'])
def twitter():
    url = "https://peerreach.p.rapidapi.com/user/lookup.json"

    querystring = {"screen_name":"audubonsociety"}

    headers = {
    'x-rapidapi-key': "0fe3a85372mshec4ebae6a3667a4p169becjsn644301488221",
    'x-rapidapi-host': "peerreach.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    name = response.json().get('screen_name')
    lastupdate = response.json().get('lastupdate')
    profiles = response.json().get('profiles')
    followers = response.json().get('followers')
    print(response.text)
    return render_template('tweet.html', response=response, name=name, profiles=profiles, lastupdate=lastupdate, followers=followers)

@app.route('/easteregg')
def Easter():
    return render_template("easteregg.html")
@app.route('/Responses/')
def Responses():
    return render_template("Responses.html")