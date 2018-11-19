import json
import requests


import pandas as pd
import datetime
from datetime import datetime
from requests.auth import HTTPBasicAuth

#from static.src.utils import *
#from static.src.utils import return_limit, dizionario_limite,\
#                             centraline

def return_limit(x):
    """Returns the standardized values of the series"""
    dizionario_limite = {'BENZENE': 5,
                         'NO2': 200,
                         'O3': 180, 
                         'PM10': 50, 
                         'PM2.5': 25}
    return dizionario_limite[x]


def make_API_auth_request(API_endpoint, query, auth, year, agenti, centraline):
    """This function makes a post requests and 
    returns and saves a dataframe. It asks for
    data referring to the specified year.
    
    :year: is the string representing the year of interest.
    :API_endpoint: the url to meke the request.
    :query: body of the post request.
    :auth: credentials.
    :agenti: list of pullutants
    :dizionario_limite: (key, value):(pollutant, limit_value)"""
    
    # Make the request
    r = requests.post(API_endpoint + '/search', 
                      auth=HTTPBasicAuth(auth['user'], auth['psw']),
                      data=query,
                      headers = {'Content-Type': 'application/json'})
    
    # Create the df with request content
    df = pd.DataFrame(json.loads(r.text))
    
    # Rename df's columns
    df.rename(index=str, 
              columns={'centralina_2': 'Preneste',
                       'centralina_3': 'Francia',
                       'centralina_5': 'Magna Grecia',
                       'centralina_8': 'Cinecitta',
                       'centralina_39': 'Villa Ada',
                       'centralina_40': 'Castel di Guido',
                       'centralina_41': 'Cavaliere',
                       'centralina_47': 'Fermi',
                       'centralina_48': 'Bufalotta',
                       'centralina_49': 'Cipro',
                       'centralina_55': 'Tiburtina',
                       'centralina_56': 'Arenula',
                       'centralina_57': 'Malagrotta'},
              inplace=True)
    
    df = df[df['inquinante'].isin(agenti)]
    df['data_ora_time'] = df.data_ora.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date())
    
    #with open(default_info_path + 'limiti_inquinanti.json') as f:
    #    dizionario_limite = json.load(f)
    df['limite'] = df.inquinante.apply(return_limit)
    # Standardize the values
    for c in centraline:
        df[c] = df[c]/df['limite']*100
    
    
    # Save the df to a csv
    df.to_csv('static/data/pregressi/data_' + year + '.csv',
              sep='\t',
              index=None)
    
    return df