from flask import Flask, render_template, session, redirect, url_for, escape, request
from models.crud import *

import json
from sendmail import sendEmails
from os import makedirs,chdir,path,stat
from subprocess import call
from bson.objectid import ObjectId

app = Flask(__name__)


@app.route('/')
def index():
	response = {}
	if 'id' in session:
		userId = session['id']
		current_user = find_unique({'_id':ObjectId(userId)},'users')
		response['message'] = current_user['userName']
		proj_list = []
		for i in current_user['projects']:
			proj_list.append(find_unique({'_id':ObjectId(i)},'projects'))
		print proj_list
		#proj_list = find({ "members" : userId } , 'projects')
		return render_template('userdashboard.html',user=current_user,proj_list = proj_list)
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

@app.route('/check_members', methods=['POST'])
def checkMembers():
	username = request.form['member_name'];
	m = find_unique({'userName': username}, 'users')
	if m:
		return json.dumps({"status": True, "id": str(m['_id'])})
	else:
		return json.dumps({"status": False})

@app.route('/create_project',methods=['POST'])
def createProject():
	print 'Hello'

	document = request.get_json()
	document['projectMembers'].append(session['id'])
	document['owner'] = session['id']

	project_id = insert(document,'projects').inserted_id

	for i in document['projectMembers']:
		temp_update = update(i,{"$push":{'projects':str(project_id)}},'users')
	
	makedirs('projects/' + str(project_id))
	chdir('projects/' + str(project_id))
	call(['git','init'],shell=False);
	return redirect(url_for('projectDashBoard',id=project_id))

# @app.route('/projectDashBoard/<id>')
# def projectDashBoard(id):
#     project = find_project_by_id(id)
#     return render_template('project_dashboard.html',project=project)

# @app.route('/projectDashBoard')
# def projectDashBoard_1():
#     return render_template('project_dashboard.html')

@app.route('/project_dashboard')
def projectDashBoard():
	return render_template('project_dashboard.html')

@app.route('/rename',methods = ['POST'])
def rename():
	proj_name = request.form['proj_name']

@app.context_processor
def override_url_for():
	return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
	if endpoint == 'static':
		filename = values.get('filename', None)
		if filename:
			file_path = path.join(app.root_path,endpoint, filename)
			values['q'] = int(stat(file_path).st_mtime)
	return url_for(endpoint, **values)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

"""if __name__ == "__main__":
	print __name__
	print app
	print Flask
	app.run()
	print __name__
	print app"""
