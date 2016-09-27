from flask import Flask, render_template, session, redirect, url_for, escape, request
from models.crud import *

import json
from sendmail import sendEmails
import os

app = Flask(__name__)


@app.route('/')
def index():
    if 'id' in session:
        userId = session['id']
        proj_list = find_project(userId, 'project')

        return render_template('userdashboard.html', proj_list=proj_list)

    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def acceptSignUp():
    if request.method == 'POST':

        fullname = request.form['fullName']
        username = request.form['userName']
        email = request.form['email']
        password = request.form['password']


        response = {}

        document = {
            "fullName": fullname,
            "userName": username,
            "email": email,
            "password": password,
        }

        result1 = find({"email": email}, 'users')
        result2 = find({"userName": username}, 'users')

        if result1.count() == 0 and result2.count() == 0:

            insert(document, 'users');
            direct_add = find_unique(document, 'users')

            os.makedirs("user/" + str(direct_add['_id']))
            session['id'] = str(direct_add['_id'])

            response['status'] = 0
            response['message'] = "Registration successful"

            return redirect(url_for('index'))

        else:
            response['status'] = 1
            if result1.count() == 0:
                response['message'] = "Username already exists"

            else:
                response['message'] = "Email already exists"
                return json.dumps(response)

    else:
        return render_template("index.html")


@app.route('/login', methods=['POST', 'GET'])
def log_in():

    response = {}

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        document1 = {
            'email': username,
            'password': password,
        }

        document2 = {
            'userName': username,
            'password': password,
        }

        result1 = find_unique(document1, 'users')
        result2 = find_unique(document2, 'users')

        if result1 != None or result2 != None:
            response['status'] = 0
            response['message'] = "Login successful"

            if result1 != None:
                session['id'] = str(result1['_id'])
            else:
                session['id'] = str(result2['_id'])

            return redirect(url_for('index'))

        else:
            response['message'] = "Invalid username and password"
            return json.dumps(response)

    else:
        response['status'] = 1
        response['message'] = "Request message not post"
        return json.dumps(response)


@app.route('/logout')
def log_out():
    session.pop('id', None)
    return render_template("index.html")


@app.route('/checkMembers', methods=['POST'])
def checkMembers():
    username = request.form['member_name'];
    m = find_unique({'userName': username}, 'users')

    if m:
        return json.dumps({"status": True})
    else:
        return json.dumps({"status": False})


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

"""if __name__ == "__main__":
<<<<<<< HEAD
    print __name__
    print app
    print Flask
    app.run()
    print __name__
    print app"""
# app.run()
