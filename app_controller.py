from flask import Flask, render_template, session, redirect, url_for, escape, request
from models.crud import *

import json
from sendmail import sendEmails
from os import makedirs,chdir
from subprocess import call

app = Flask(__name__)


@app.route('/')
def index():
    response = {}
    if 'id' in session:
        userId = session['id']
        # response = {}
        response['message'] = "suhavan"
        proj_list = find_project(userId, 'project')
        return render_template('userdashboard.html', proj_list=proj_list, response=response)

    else:
        return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def acceptSignUp():
    response = {}
    if request.method == 'POST':

        fullname = request.form['fullName']
        username = request.form['userName']
        email = request.form['email']
        password = request.form['password']

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

            makedirs("user/" + str(direct_add['_id']))
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
    return redirect(url_for('index'))

@app.route('/checkMembers', methods=['POST'])
def checkMembers():
    username = request.form['member_name'];
    m = find_unique({'userName': username}, 'users')
    if m:
        return json.dumps({"status": True, "id": str(m['_id'])})
    else:
        return json.dumps({"status": False})

@app.route('/createProject',methods=['POST'])
def createProject():

    document = {}
    document['project_name'] = request.form['project_name']
    document['project_description'] = request.form['project_description']
    document['project_members'] = request.form['project_members']

    project_id = insert(document,'projects')

    makedirs('projects/' + str(project_id))
    chdir('projects/' + str(project_id))
    call(['git','init'],shell=False);

    return redirect(url_for('projectDashBoard',id=project_id))

@app.route('/projectDashBoard/<id>')
def projectDashBoard(id):

    project = find_project_by_id(id)
    return render_template('project_dashboard.html',project=project)



app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

"""if __name__ == "__main__":
    print __name__
    print app
    print Flask
    app.run()
    print __name__
    print app"""
# app.run()
