from connect import db
from bson.objectid import ObjectId


users = db.users
projects = db.projects


def insert(document,collection_name):
	if collection_name == "projects":
		return projects.insert_one(document)
	else:
		return users.insert_one(document)

def find(document,collection_name):
	if collection_name == "projects":
		return projects.find(document)

	else:
		return users.find(document)

def find_unique(document,collection_name):
	if collection_name == "projects":
		return projects.find_one(document)
	else:
		return users.find_one(document)

def update(id,modify,collection_name):
	if collection_name == "projects":
		#upseert false will insert a new document is id not found
		return projects.update({'_id':ObjectId(id)}, modify, upsert = False)
	else:
		return users.update({'_id':ObjectId(id)}, modify, upsert = False)

def delete(document,collection_name):
	if collection_name == "projects":
		return projects.delete_one(document)
	else:
		return users.delete_one(document)
