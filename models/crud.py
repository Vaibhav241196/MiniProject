from connect import db

users = db.users
projects = db.projects


def insert(document,collection_name):
	if collection_name == "projects":
		return projects.insert_one(document)
	else:
		return users.insert_one(document)

def find(document,collection_name):
	if collection_name == "project":
		return projects.find(document)

	else:
		return users.find(document)

def find_unique(document,collection_name):
	if collection_name == "project":
		return projects.find_one(document)
	else:
		return users.find_one(document)

