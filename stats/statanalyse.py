# -*- coding: utf-8 -*-
import json
import datetime
import os
import glob
from pprint import pprint


timestamp = datetime.datetime.now().strftime('%Y%m%d:%H%M%S')
filename = 'data-' + str(timestamp) + '.json'

def generate_new_import():
    os.system("mongoexport --host ds063307.mongolab.com --port 63307 --username edelans --password nomorebooks -d exercix -c exercix  --jsonArray --out "+filename)


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

data_file_list = glob.glob('data-*.json')
data_file_list = sorted(data_file_list, reverse=True)
last_filename = data_file_list[0]

with open(last_filename) as data_file:
    data = json.load(data_file)
    #objets où on va stocker les données:
    users        =[] #set d'adresses mail
    track        ={"MP":0,"PC":0,"PSI":0} #stocker les filières
    prepas       ={}
    departements ={}
    viewcounts   ={}
    flags        ={}
    for record in data:
        users.append(record["mail"])
        track[record["filiere"]]+=1
        # enregistrement des prepas
        dictadd("nomprepa",prepas)
        dictadd("zipcode",departements, True)
        for view in record["data"]["viewcounts"]:
            if len(view["id"])==24:
                if view["id"] in viewcounts.keys():
                    viewcounts[view["id"]]+=1
                else:
                    viewcounts[view["id"]]=1
    output={
        "date":datetime.datetime.now(),
        "nbusers":len(users),
        "repartition_filiere":track,
        "prepas_users":prepas
    }

def generate_new_export():
    os.system("mongoimport --host ds063307.mongolab.com --port 63307 --username edelans --password nomorebooks -d exercix -c stats  --jsonArray --file "+filename)


generate_new_import()
generate_new_export()

if __name__ == '__main__':
    print "#"*80
    pprint(output)
    print "#"*80
