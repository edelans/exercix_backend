#-*- coding: utf-8 -*-
import datetime
from pprint import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.dbref import DBRef

### Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname
MONGODB_URI = 'mongodb://edelans:nomorebooks@ds063307.mongolab.com:63307/exercix'
client = MongoClient(MONGODB_URI)
db = client.exercix

records=db['exercix']
stats=db['stats']
improver = db['improver']


raw_data = records.find()
improve_data = improver.find()


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





#objets où on va stocker les données:
users        =[]  #set d'adresses mail
track        ={"MP":0,"PC":0,"PSI":0} #stocker les filières
prepas       ={}
OS           ={"android":{}, "ios":{}}
views        ={}
nbviewsL7D   =0
activeUsersL7D=[]
improvements =[]

#js timestamp
now = int((datetime.datetime.now()-datetime.datetime(1970,1,1)).total_seconds())


for record in raw_data:
    #enregistrement des mails
    users.append(record["mail"])


    #enregistrement des filières: parfois le champ n'est pas renseigné alors on prend des précautions
    try:
        track[record["filiere"]]+=1
    except:
        pass

    # enregistrement des prepas
    dictadd("nomprepa",prepas)


    #enregistrement de l'OS et de la version
    if "OS" in record:
        OSrec = record["OS"].lower().split()  #OSrec est une liste du genre ["iOS", "ver", "7.0"]
        try:
            OS[OSrec[0]][OSrec[2].replace('.','p')]+=1
        except KeyError:
            OS[OSrec[0]][OSrec[2].replace('.','p')]=1

    #traitement des viewcounts
    for view in record["data"]["viewcounts"]:
        try:
            if view["id"] in views.keys():
                views[view["id"]].append(view["date"])
            else:
                views[view["id"]] = [view["date"]]
            if view["date"] > now - 7*24*60*60:
                nbviewsL7D +=1
                activeUsersL7D.append(record["mail"])
        except TypeError:
            pass

    #traitement des flags
    try:
        for flag in record["data"]["flags"]:
            if improver.find({"$and":[ {"date":flag['date']}, {"msg":flag['msg']}]}).count()==0:
                improvement = {
                    "exo":DBRef('exo', ObjectId(flag['id']), database='exercix'),
                    "date":flag['date'],
                    "msg":flag['msg'],
                    "processed":False
                    }
                improver.insert(improvement)
                improvements.append(improvement)
    except KeyError:
        pass #parfois il n'y a pas de flag


# on enregistre tout dans le dico à uploader sur mongolab
output={
    "date":datetime.datetime.now(),
    "nbusers":len(users),
    "repartition_filiere":track,
    "prepas_users":prepas,
    "platform":OS,
    "views":views,
    "nbviewsL7D":nbviewsL7D,
    "activeUsersL7D":len(set(activeUsersL7D))
}


stats.insert(output)

if __name__ == '__main__':
    print "#"*80
    pprint(output)
    print "-"*80
    pprint(improvements)
    print "#"*80

