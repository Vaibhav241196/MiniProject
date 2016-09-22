from flask import Flask,render_template,request,url_for
from models.crud import insert,find,find_unique
import json

from sendmail import sendEmails

import os


app = Flask(__name__)   

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/signup', methods=['GET','POST'])
def acceptSignUp():
    
	if request.method == 'POST':

	    fullname=request.form['fullName']
	    username=request.form['userName']
	    email=request.form['email']
	    password=request.form['password']
	    repeatpassword=request.form['repeatPassword']
	    termscheck=request.form['termsCheck']

	    response = {}

	    document = {
	    				"fullName" : fullname,
	    				"userName" : username,
	    				"email" : email,
	    				"password" : password,
	               }

	    result1 = find({"email" : email },'users')
	    result2 = find({"userName":username},'users')


	    if result1.count() == 0 and result2.count() == 0:

	    	insert(document,'users');
	    	#print direct_add
	    	direct_add = find_unique(document,'users')
	    	print direct_add
	    	os.mkdir("user/"+str(direct_add['_id']))
	    	response['status'] = 0
	    	response['message'] = "Registration successful"
	    	return render_template('userdashboard.html',response = response)


	    else:
	    	response['status'] = 1
	    	if result1.count() == 0:
	    		response['message'] = "Username already exists"
	    	else:
	    		response['message'] = "Email already exists"  
	    	return render_template('index.html',response = response)
	    #return json.dumps(response)

	else:
		return render_template("index.html")


@app.route('/login',methods = ['POST','GET'])
def log_in():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		document = {
					'email':username,
					'password' : password,
					}
		response = {}
		print document
		result = find(document,'users')
		print result
		if result.count() == 0:
			document = {
						'userName':username,
						'password':password,
						}
			result = find(document,'users')
			if result.count() == 0:
				response['message'] = "Invalid username and password"
				return render_template("index.html",response = response)
			else:
				response['message'] = "Login Successful"
				return json.dumps(response)
				#return render_template("userdashboard.html",response)
		else:
			response['message'] = "Login successful"
			return render_template("userdashboard.html",response = response)

		#return json.dumps(response)
	else:
		return render_template("index.html")

@app.route('/dump')
def dump_page():
	response = {}
	response['message'] = "Login successful"
	return render_template("userdashboard.html",response = response)



"""if __name__ == "__main__":
    print __name__
    print app
    print Flask
    app.run()
    print __name__
    print app"""
