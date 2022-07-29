
import subprocess
import os
import pandas as pd
import numpy as np
from os.path import dirname as parent_dir
from os.path import join as join


from datetime import datetime

import requests
import json

try:
    find_my_parent = parent_dir(parent_dir(parent_dir(os.path.realpath(__file__))))
except:
    find_my_parent = parent_dir(parent_dir(os.path.abspath('__file__')))


def get_johns_hopkins():
    ''' Get data by a git pull request, the source code has to be pulled first
        Result is stored in the predifined csv structure
    '''

    raw_data_path = join(find_my_parent,"data","raw","COVID-19")
    print(raw_data_path)

    git_pull = subprocess.Popen( "git pull" ,
                         cwd = raw_data_path,
                         shell = True,
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE )
    (out, error) = git_pull.communicate()


    print("Error : " + str(error))
    print("out : " + str(out))


def get_current_data_germany():
    ''' Get current data from germany, attention API endpoint not too stable
        Result data frame is stored as pd.DataFrame
    '''
    # 16 states
    #data=requests.get('https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json')

    # 400 regions / Landkreise
    data=requests.get('https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json')

    json_object=json.loads(data.content)
    full_list=[]
    for pos,each_dict in enumerate (json_object['features'][:]):
        full_list.append(each_dict['attributes'])

    pd_full_list=pd.DataFrame(full_list)
    final_path = join(find_my_parent,"data","raw","NPGEO","GER_state_data.csv")
    pd_full_list.to_csv(final_path,sep=';')
    print(' Number of regions rows: '+str(pd_full_list.shape[0]))

if __name__ == '__main__':
    get_johns_hopkins()
    get_current_data_germany()