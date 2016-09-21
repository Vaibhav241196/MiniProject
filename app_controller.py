from flask import Flask,render_template,request,url_for
from models.crud import insert,find
import json

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

	    result = find({"email" : email })

	    if(result.count() == 0):
	    	insert(document);
	    	response['status'] = 0;
	    	response['message'] = "Registration successful";

	    else:
	    	response['status'] = 1;
	    	response['message'] = "Email already exists";
	    

	    return json.dumps(response)

	else:
		return "Hello world"


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
		result = find(document)
		print result
		if result.count() == 0:
			response['message'] = "Invalid username and password"
		else:
			response['message'] = "Login successful"

		return json.dumps(response)
	else:
		return json.dumps("Fuck Off")


"""if __name__ == "__main__":
    print __name__
    print app
    print Flask
    app.run()
    print __name__
    print app"""

