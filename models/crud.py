from connect import db

users = db.users

def insert(document):
	users.insert_one(document)