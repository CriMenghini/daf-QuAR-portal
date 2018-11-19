
import ast
import copy
import json
import requests
import datetime
import subprocess


import numpy as np
import pandas as pd
import geopandas as gp
from geopandas.geoseries import *
from shapely.geometry import Point
from requests.auth import HTTPBasicAuth


from static.src.inquinanti import Inquinante
from static.src.map_data import color_bubbles, bar_plot, \
                                pie_plot
from static.src.data_request import make_API_auth_request



# Open files to get default informations
default_info_path = 'static/data/default_info/'
with open(default_info_path + 'agenti_format.json') as f:
    agenti_format = json.load(f)

with open(default_info_path + 'limiti_inquinanti.json') as f:
    dizionario_limite = json.load(f)
    
with open(default_info_path + 'agenti_e_centraline.json') as f:
    agenti_centraline = json.load(f)
    agenti = agenti_centraline['inquinanti']
    centraline = agenti_centraline['centraline']

with open(default_info_path + 'methods.json') as f:
    method_index = json.load(f)

# Get the current year
current_year = str(datetime.datetime.now().year)

# Format the query
query = json.dumps({"select": [{"name": "ora"},
                               {"name": "anno"},
                               {"name": "data_ora"},
                               {"name": "inquinante"},
                               {"name": "centralina_2"},
                               {"name": "centralina_3"},
                               {"name": "centralina_5"},
                               {"name": "centralina_8"},
                               {"name": "centralina_39"},
                               {"name": "centralina_40"},
                               {"name": "centralina_41"},
                               {"name": "centralina_47"},
                               {"name": "centralina_48"},
                               {"name": "centralina_49"},
                               {"name": "centralina_55"},
                               {"name": "centralina_56"},
                               {"name": "centralina_57"}],
                    
                    "where": {'or':[{"eq": {"left": "anno", "right": current_year}}]}
                   })

# Get the credentials from a txt file
with open('static/data/auth/credential.txt') as f:
    credentials = f.read().split()
    auth = {}
    auth['user'] = credentials[0]
    auth['psw'] = credentials[1]
    API_endpoint = credentials[2]
    
# Do the request
# Do the request

check = False
while check == False:
    try:
        df = make_API_auth_request(API_endpoint, 
                               query, 
                               auth, 
                               current_year,
                               agenti,
                               centraline)
        check = True
    except:
        print ('API error, execute again!')
        continue


# Define the dictionary of Inquinante objects
inq_objects = {a: Inquinante(a, dizionario_limite[a], method_index[a]) 
               for a in agenti}

print (inq_objects['BENZENE'])

# Create the topojson for the map
# Bubbles color
colori_dict, valori_dict, list_df = color_bubbles(df, current_year, \
                                                  dizionario_limite, \
                                                  method_index, \
                                                  centraline, \
                                                  inq_objects)



# Bar plot data
list_bars = bar_plot(list_df, centraline)
# Pie data
lista_centrali_2 = pie_plot(df, centraline)

# Load file
roma = pd.read_csv('static/data/default_info/arpaaria.csv', sep=';')
# Seleziona centraline roma
roma = roma[roma["Localita'"] == 'Roma']
# Clean lat e lon columns (replace , with points)
roma['lat'] = roma.Latitudine.apply(lambda x: float(x.split('.')[0]
                                                    +'.'
                                                    +''.join(x.split('.')[-2:])))
roma['lon'] = roma.Longitudine.apply(lambda x: float(x.split('.')[0]
                                                     +'.'
                                                     +''.join(x.split('.')[-2:])))
roma['livelloInquinamento'] = roma.Nome.apply(lambda x: colori_dict[x])
roma['valoreInquinanti'] = roma.Nome.apply(lambda x: list_bars[x][0])
roma['valCentr'] = roma.Nome.apply(lambda x: int(valori_dict[x]))
roma['valPie'] = roma.Nome.apply(lambda x: str(lista_centrali_2[x]).replace("'", '"'))
roma['Coordinates'] = list(zip(roma.lon, roma.lat))
roma['Coordinates'] = roma['Coordinates'].apply(Point)

# Greate the shapefile
gdf = gp.GeoDataFrame(roma, geometry='Coordinates')
del gdf['Latitudine'], gdf['Longitudine']

gdf.crs = {'init': 'epsg:4326', 'no_defs': True}
gdf.to_crs(epsg=4326, inplace=True)
gdf.to_file('shape_files/stazioni.shp')

# Create the topojson
bashCommand = "mapshaper -i shape_files/*.shp snap combine-files -o static/data/mappa/output-topo.json format=topojson"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()


print ('The server is ready')


