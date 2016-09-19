from connect import db

users = db.users

def insert(document):
	print __name__
	return users.insert_one(document)

def find(document):
	return users.find(document)
