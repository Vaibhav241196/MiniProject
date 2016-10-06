from flask import Flask, render_template, session, redirect, url_for, escape, request, send_from_directory
from models.crud import *

import json
from sendmail import sendEmails
from os import makedirs, chdir, path, stat, listdir, curdir, remove, getcwd, mknod
from shutil import rmtree
from subprocess import call, check_output
from bson.objectid import ObjectId

app = Flask(__name__)


# function for home page route using session for automatic log in
@app.route('/')
def index():
    if 'id' in session:
        return redirect(url_for('user_dashboard'))
    else:
        return render_template("index.html")

# function for rendering user dashboard page
# using user id for getting the logged in user
@app.route('/user_dashboard')
def user_dashboard():

    print "Hello in user dashboard"
    userId = session['id']
    current_user = find_unique({'_id': ObjectId(userId)}, 'users')

    response = {}
    response['message'] = current_user['userName']

    proj_list = []
    count = {}
    if 'projects' in current_user:
        for i in current_user['projects']:
            project = find_unique({'_id': ObjectId(i)}, 'projects')
            if project != None:
                proj_list.append(project)

                # proj_list = find({ "members" : userId } , 'projects')

    # allProjects = proj_list[].__len__()

    value_myProjects = 0
    value_totalProjects = len(proj_list)

    myProjects = aggregate(str(userId), 'projects')

    for j in myProjects:
        value_myProjects = j['count']

    count['allProjects'] = value_totalProjects
    count['myProjects'] = value_myProjects
    count['sharedProjects'] = value_totalProjects - value_myProjects

    myProjects_domain = aggregate_domain(str(userId), 'projects')

    for i in myProjects_domain:
        count.update({i['_id']: i['count']})

    print count
    print "Hello"
    return render_template('userdashboard.html', user=current_user, proj_list=proj_list, count=count)


@app.route('/signup', methods=['GET', 'POST'])
def accept_signup():
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
def check_members():
    username = request.form['member_name'];
    m = find_unique({'userName': username}, 'users')

    if m:
        if str(m['_id']) == session['id']:
            return json.dumps({"status": 1, "message": "You are the owner of the project"})

        return json.dumps({"status": 0, "id": str(m['_id']), "message": "Member added successfully"})

    else:
        return json.dumps({"status": 2, "message": "No such user found"})

# creates new project and redirects to the project home page
@app.route('/create_project', methods=['POST'])
def create_project():
    print 'Hello'

    document = request.get_json()
    document['projectMembers'].append(session['id'])
    document['owner'] = session['id']
    document['branches'] = [{'branch_name' : 'master' , 'members' : [ session['id'] ] }]

    project_id = insert(document, 'projects').inserted_id

    for i in document['projectMembers']:
        temp_update = update(i, {"$push": {'projects': str(project_id)}}, 'users')

    makedirs(path.join(app.root_path,'../projects', str(project_id) ))
    chdir(path.join(app.root_path,'../projects', str(project_id) ))
    call(['git', 'init'], shell=False)
    call(['git','commit','--allow-empty','-m','"Initial Empty Commit"'],shell=False)

    return json.dumps({ 'id': str(project_id) } )

# function to create new file and folders
@app.route('/create_new', methods=['POST'])
def create_file():
    name = request.form['name']
    type = request.form['type']

    if type == 'new-folder':
        makedirs(name)

    elif type == 'new-file':
        mknod(name)

    return json.dumps({'status': 0 , 'message': "File created successfully" })

# function to return the dictionary with the given branch name
def return_members(branch_dict, branch_name):
    if branch_dict['branch_name'] == branch_name:
        return branch_dict['members']
    else:
        return


# function to return whether the user has access for the branch or not
# 1 means he has the access
# 0 means permission denied
def check_access(proj_id):
    user_id = session['id']
    print proj_id
    current_project = find_unique({'_id': ObjectId(proj_id)},'projects')
    current_user = find_unique({'_id': ObjectId(user_id)},'users')
    branch_name = check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], shell=False)[:-1]
    branch_members = filter(lambda x: return_members(x, branch_name), current_project['branches'])
    if str(user_id) == current_project['owner']:
        return 1
    elif str(user_id) in branch_members:
        return 1
    else:
        return 0


# function to return the list of directories and files in the current directory
def return_list():
    curr_files = listdir(curdir)  # list of files and directories
    print curr_files

    list_dir = {
        'files': filter(path.isfile, curr_files),  # list of files
        'directories': filter(path.isdir, curr_files),
    }

    if '.git' in list_dir['directories']:
        list_dir['directories'].remove('.git')

    list_dir['directories'].sort()
    list_dir['files'].sort()

    return list_dir


# Function to render project dashboard home page on get request and
# to traverse through files and folders and post request

@app.route('/project_dashboard/<id>', methods=['GET','POST'])
def project_dashboard(id):

    print "Hello"

    project_path = path.join(app.root_path,'../projects', id)

    if request.method == 'GET':
        project = find_unique({'_id': ObjectId(id)}, 'projects')
        members = []

        for m in project['projectMembers']:
            user = find_unique({ '_id': ObjectId(m) },'users')
            members.append(user)

        chdir(project_path)

        list_dir = return_list()
        return render_template('project_dashboard.html', project=project, members=members , list_dir=list_dir)

    elif request.method == 'POST':
        dir_path = request.form['dir_path']
        chdir(dir_path)
        list_dir = return_list()

        l = len(project_path)
        list_dir['current'] = getcwd()[l:]

        return json.dumps(list_dir)


# function to change branch input (project id,branch name)
# returns the list of folders and files after git checkout
@app.route('/checkout', methods=['POST'])
def change_branch():
    proj_id = request.form['proj_id']
    change_branch = request.form['branch_name']
    chdir(path.join(app.root_path,'../projects',str(proj_id)))
    temp = call(['git', 'checkout', str(change_branch)], shell=False)
    response = {}
    if temp == 1:
        response['status'] = 1
        response['message'] = 'Please, commit your changes before you can switch branches.'
    else:
        response['status'] = 0
        response['message'] = 'Switching to ' + str(change_branch)

    list_dir = return_list()
    return json.dumps({'list_dir': list_dir, 'response': response })


# function to create new git branch input (project id,new branch name)
# returns status and message
# also make sures that the user is owner of the project
# incomplete
@app.route('/new_branch', methods=['POST'])
def create_branch():

    print "In create branch"
    branch_data = request.get_json()
    proj_id = branch_data.pop('id',None)

    print proj_id
    project = find_unique({'_id': ObjectId(proj_id)},'projects')
    print project
    print branch_data
    response = {}

    if project['owner'] == session['id']:
        chdir(path.join(app.root_path,'../projects', proj_id))
        temp = call(['git', 'branch', str(branch_data['branch_name'])], shell=False)
        update(proj_id,{'$push' : { 'branches' : branch_data }},'projects')

        if temp == 0:
            response['status'] = 0
            response['message'] = 'Branch successfully created'
        else:
            response['status'] = 1
            response['message'] = 'Choose another name'
    else:
        response['status'] = 1
        response['message'] = 'Permission denied'

    return json.dumps(response)


# function to return the list of files and folders
# input (project id, path)
# path = address of folder relative to projects/project id
@app.route('/path', methods=['POST'])
def return_files():
    proj_id = request.form['id']
    path = request.form['path']
    chdir(path.join(app.root_path,'../projects',str(proj_id),path))
    list_dir = return_list()
    return json.dumps(list_dir)


# function to delete the file or folder
# input (project id,path)
# path format is same as in the above function
@app.route('/delete_path', methods=['POST'])
def delete_files():
    proj_id = request.form['id']
    path = request.form['path']
    current_project = find_unique({'_id': ObjectId(proj_id)}, projects)
    current_user = find_unique({'_id': ObjectId(session['_id'])}, users)
    response = {}
    if check_access(proj_id):
        try:
            remove(path.join(app.root_path,'../projects' ,str(proj_id),str(path)))
        except:
            rmtree(path.join(app.root_path,'../projects' ,str(proj_id),str(path)))
        response['status'] = 0
        response['message'] = 'Successfully deleted'
    else:
        response['status'] = 1
        response['message'] = 'Permission Denied'
    return json.dumps(response)


# function to download files and folder
# input (project id,path)
# path format is same as in the above functions
@app.route('/download_path', methods=['POST'])
def download_path():
    proj_id = request.form['id']
    path = request.form['path']
    call(['tar', '-czvf', path.join(app.root_path , '../projects', str(proj_id) ,'.tar.gz'), path.join(app.root_path,'../projects',str(proj_id) , str(path))], shell=False)
    temp_path = path.join(app.root_path , '../projects')
    return send_from_directory(directory=temp_path, filename=str(proj_id) + '.tar.gz')


# function to commit the changes
# input (project id,commnt message)
@app.route('/commit', methods=['POST'])
def commit_changes():
    proj_id = request.form['id']
    message = request.form['message']
    response = {}
    if check_access(proj_id):
        call(['git', 'add', '.'], shell=False)
        call(['git', 'commit', '-m', str(message)], shell=False)
        sha_id = check_output(['git', 'rev-parse', 'HEAD'], shell=False)
        if find_unique({'sha_id': sha_id}, 'commits'):
            response['message'] = "Nothing to commit"
            response['status'] = 1
        else:
            response['message'] = "Commit Successful"
            response['status'] = 0
            document = {
                'sha_id': sha_id,
                'branch': check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], shell=False)[:-1],
                'project': str(proj_id),
                'comment': str(message)
            }
            insert(document, 'commits')
    else:
        response['message'] = "Permission denied"
        response['status'] = 1
    return json.dumps(response)


# function to return the list of commit logs
# input (project id)
@app.route('/commit_log', methods=['POST'])
def commit_log():
    document = {
        'proj_id': request.form['id'],
        'branch': check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], shell=False)[:-1]
    }
    log = find(document, 'commits')
    return json.dumps(log)

# function to return the contents of file
# input (project id,path)
@app.route('/edit', methods=['POST'])
def edit_file():
    # proj_id = request.form['id']
    path = request.form['path']
    location =  str(path)

    fileobject = open(location, "r")
    loadbuffer = fileobject.read()
    fileobject.close()
    return loadbuffer


# function to save the contents of the file
# input (project id, path, content of the file)
@app.route('/save', methods=['POST'])
def save_file():
    proj_id = request.form['proj_id']
    path = request.form['path']
    code = request.form['code']
    response = {}

    if check_access(proj_id):
        location =  str(path)
        fileobject = open(location, "w")
        fileobject.write(code)
        fileobject.close()
        response = {
            'status': 0,
            'message': 'Successfully overwritten '
        }
    else:
        response = {
            'status': 1,
            'message': 'Permission Denied'
        }
    return json.dumps(response)

# @app.route('/projectDashBoard')
# def projectDashBoard_1():
#     return render_template('project_dashboard.html')

# @app.route('/project_dashboard')
# def project_dashboard():
#     return render_template('project_dashboard.html')


@app.route('/rename', methods=['POST'])
def rename():  # yet to be integrated
    proj_id = request.form['proj_id']
    new_name = request.form['new_name']
    update_project = update(proj_id, {'$set': {'projectName': str(new_name)}}, 'projects')
    return json.dumps({'status': 1, 'message': 'Successfully renamed', 'new_name': new_name})


# we havent deleted the follder

    # userId = session['id']
    # current_user = find_unique({'_id': ObjectId(userId)}, 'users')
    #
    # proj_list = []
    #
    # if 'projects' in current_user:
    #     for i in current_user['projects']:
    #         proj_list.append(find_unique({'_id': ObjectId(i)}, 'projects'))
    #         # return render_template('userdashboard.html',user=current_user,proj_list = proj_list)
    # return json.dumps({'user': current_user, 'proj_list': proj_list})
    # return json.dumps({'status': 1, 'message': 'Successfully renamed', 'new_name': new_name})

@app.route('/delete', methods=['POST'])
def remove():
    proj_id = request.form['proj_id']
    userId = session['id']

    response = {}

    project = find_unique({'_id': ObjectId(proj_id)}, 'projects')
    print project['owner']
    print userId

    if project['owner'] == userId:
        for i in project['projectMembers']:
            temp_update = update(i, {'$pull': {'projects': str(proj_id)}}, users)
        temp = delete({'_id': ObjectId(proj_id)}, 'projects')
        response['status'] = 0
        response['message'] = "Successfully deleted"
        #projectMembers = find({'projects': str(proj_id)}, 'users')

        for i in project['projectMembers']:
            update_users = update(i, {'$pull' : {'projects' : str(proj_id)}} , 'users')
    else:
        response['status'] = 1
        response['message'] = "Only owner can delete a project"

    # proj_list = []

    # if 'projects' in current_user:
    #     for i in current_user['projects']:
    #         proj_list.append(find_unique({'_id': ObjectId(i)}, 'projects'))
    #         # return render_template('userdashboard.html',user=current_user,proj_list = proj_list)

    return json.dumps(response)


# print app.config['MODELS']
@app.route('/download', methods=['GET', 'POST'])
def download():  # extension problem
    proj_id = request.form['download-project-id']
    call(['tar', '-czvf', path.join(app.root_path,'../projects' , str(proj_id) ,'.tar.gz') , path.join(app.root_path,'../projects',str(proj_id)) ] ,shell=False)
    temp_path = path.join(app.root_path + '../projects')
    return send_from_directory(directory=temp_path, filename=str(proj_id) + '.tar.gz')


# function to send request for project
# function will be called when the user sends the request to show his/her interest in the project while searching
# input(project id)
@app.route('/apply', methods=['POST'])
def apply_proj():
    proj_id = request.form['proj_id']
    user_id = session['id']
    current_project = find_unique({'_id': ObjectId(proj_id)}, 'projects')
    response = {}
    if user_id not in current_project['projectMembers']:
        update(proj_id, {'$push': {'requests': str(user_id)}}, 'projects')
        response['status'] = 0
        response['message'] = 'Request successfully sent'
    else:
        request['status'] = 1
        request['message'] = 'Already a member'
    return json.dumps(request)


# function to accept or decline the notifications
# input (project_id, status,user id)
# status 1 then accept
@app.route('/notify', methods=['POST'])
def accept_decline():
    proj_id = request.form['proj_id']
    status = str(request.form['status'])
    user_id = request.form['user_id']
    update(proj_id, {'$pull': {'requests': str(user_id)}}, 'projects')
    response = {}
    if status == str(0):
        response['message'] = 'request not accepted'
        response['status'] = 0
    else:
        update(proj_id, {'$push': {'projectMembers': str(user_id)}}, 'projects')
        response['status'] = 0
        response['message'] = 'request accepted'
    return json.dumps(response)


# function to return the list of notifications
# input none
# output list of dictionaries with keys projectname and username
def notify_user():
    user_id = session['id']
    proj_list = find({'owner': str(user_id)}, 'projects')
    notify_list = []
    for i in proj_list:
        try:
            projectName = find_unique({'_id': ObjectId(i['_id'])}, 'projects')['projectName']
            for j in i['requests']:
                document = {
                    'userName': find_unique({'_id':ObjectId(j)}, 'users')['userName'],
                    'projectName': projectName
                }
                notify_list.append(document)
        except:
            print "no requests in the current project"

    return notify_list




@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = path.join(app.root_path, endpoint, filename)
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
