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



if __name__ == "__main__":
    app.run()