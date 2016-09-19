import pymongo

client = pymongo.MongoClient()
db = client.prohub_db
result_user = db.users.create_index([('user_id',pymongo.ASCENDING)],unique = True)
result_project = db.project.create_index([('project_id',pymongo.ASCENDING)],unique = True)
print "hello"
print result_user
print result_project


