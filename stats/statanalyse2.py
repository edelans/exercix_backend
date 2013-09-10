# -*- coding: utf-8 -*-
import datetime
from pprint import pprint
from pymongo import MongoClient

### Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname
MONGODB_URI = 'mongodb://edelans:nomorebooks@ds063307.mongolab.com:63307/exercix'
client = MongoClient(MONGODB_URI)
db = client.exercix

records=db['exercix']
stats=db['stats']


def dictadd(champ,dico, cut=False):
    if not cut:
        if record[champ].lower() in dico.keys():
            dico[record[champ].lower()]+=1
        else:
            dico[record[champ].lower()]=1
    if cut:
        if record[champ][:2] in dico.keys():
            dico[record[champ][:2]]+=1
        else:
            dico[record[champ][:2]]=1


data = records.find()
#objets où on va stocker les données:
users        =[] #set d'adresses mail
track        ={"MP":0,"PC":0,"PSI":0} #stocker les filières
prepas       ={}
for record in data:
    users.append(record["mail"])
    track[record["filiere"]]+=1
    # enregistrement des prepas
    dictadd("nomprepa",prepas)
output={
    "date":datetime.datetime.now(),
    "nbusers":len(users),
    "repartition_filiere":track,
    "prepas_users":prepas
}

stats.insert(output)

if __name__ == '__main__':
    print "#"*80
    pprint(output)
    print "#"*80
