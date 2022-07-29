import pandas as pd
import numpy as np
import os
from datetime import datetime

from os.path import dirname as parent_dir
from os.path import join as join


try:
    find_my_parent = parent_dir(parent_dir(parent_dir(os.path.realpath(__file__))))
except:
    find_my_parent = parent_dir(parent_dir(os.path.abspath('__file__')))



def store_relational_JH_data():
    ''' Transformes the COVID data in a relational data set
    '''

    data_path= join(find_my_parent,'data','raw','COVID-19','csse_covid_19_data','csse_covid_19_time_series','time_series_covid19_confirmed_global.csv')
    print(data_path)
    pd_raw=pd.read_csv(data_path)

    pd_data_base=pd_raw.rename(columns={'Country/Region':'country',
                      'Province/State':'state'})

    pd_data_base['state']=pd_data_base['state'].fillna('no')

    pd_data_base=pd_data_base.drop(['Lat','Long'],axis=1)


    pd_relational_model=pd_data_base.set_index(['state','country']) \
                                .T                              \
                                .stack(level=[0,1])             \
                                .reset_index()                  \
                                .rename(columns={'level_0':'date',
                                                   0:'confirmed'},
                                                  )

    pd_relational_model['date']=pd_relational_model.date.astype('datetime64[ns]')

    covid_RB_path = join(find_my_parent,"data","processed","COVID_relational_confirmed.csv")
    pd_relational_model.to_csv(covid_RB_path,sep=';',index=False)
    print(' Number of rows stored: '+str(pd_relational_model.shape[0]))

if __name__ == '__main__':

    store_relational_JH_data()