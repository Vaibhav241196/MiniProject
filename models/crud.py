from connect import db

users = db.users
project = db.project

def insert(document,collSelect):
	if collSelect == 1:
		return users.insert_one(document)
	elif collSelect == 2:
		return project.insert_one(document)

def find(document):
	return users.find(document)