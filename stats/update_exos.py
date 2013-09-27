#-*- coding: utf-8 -*-
import pymongo


### Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname
MONGODB_URI = 'mongodb://edelans:nomorebooks@ds063307.mongolab.com:63307/exercix'
client = pymongo.MongoClient(MONGODB_URI)
db = client.exercix


db.exo.update(
    {"author":{ "$ne": 'dsfsdf' }}, #query
    {"$set": { "appli": "prepasc2",  "package": "lite"}}, # modifications to apply
    upsert= False, #does not insert a new document when no match is found
    multi=True # updates multiple documents that meet the query criteri
    )


if __name__ == '__main__':
    print "#"*80
