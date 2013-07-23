import json

with open('structure.json', 'rb') as fp:  #placeholder 
        structure = json.load(fp)
print structure["parts"][0]["chapters"][0]["chapter"]