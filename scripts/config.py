import os
import json


CONFIG_PATH = 'data/config'

config = {}

for file in os.listdir(CONFIG_PATH):
    f = open(CONFIG_PATH + '/' + file, 'r')
    config[file.split('.')[0]] = json.load(fp=f)
    f.close()
        
        