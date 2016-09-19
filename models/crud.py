from connect import db

users = db.users
project = db.project

def insert(document,collection_name):
	if collection_name == "project":
		return project.insert_one(document)
	else:
		return users.insert_one(document)

def find(document,collection_name):
	if collection_name == "project":
		for i in project.find(document):
			print i._id
		return project.find(document)

	else:
		return users.find(document)
