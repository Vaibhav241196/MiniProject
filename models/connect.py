import pymongo

client = pymongo.MongoClient()
db = client.test
db.sites.insert({"name":"tejas" , "age":"21"})
