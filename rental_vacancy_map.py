# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 12:44:58 2023

@author: tai
"""

#Import Libraries
import os
import webbrowser

import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from folium.features import GeoJsonTooltip

#github scripts: https://github.com/liu3388/maps_scripts.git
#github maps csv: https://github.com/liu3388/maps_csv.git
#Census data source: https://www.census.gov/housing/hvs/index.html
#MSA geojson files: https://github.com/loganpowell/census-geojson/find/master

#%% select quarter
qtr = '3Q2022'

#%% setup path to import JSON and CSV files
# os.chdir("C:\\Tai\\RE_project\\Github\\maps\\GeoJson\\maps_GeoJson")
# path_json = os.getcwd()
# MSA_json = "MSA.json"
# df_MSA1 = gpd.read_file(path_json + "\\" + MSA_json)

# os.chdir("C:\\Tai\\RE_project\\Github\\maps\\maps_csv\\csv")
# path_csv = os.getcwd()
# vacancy_rates = "rental_vacancy.csv"
# df_vacancy = gpd.read_file(path_csv + "\\" + vacancy_rates)

# df_vacancy.drop(['geometry'], axis=1, inplace=True) #clean up last strange column

#%% fetch GeoJson and csv file on GitHub
url_GeoJson = 'https://raw.githubusercontent.com/liu3388/maps_GeoJson/main/MSA.json'
df_MSA1 = gpd.read_file(url_GeoJson)

url_vacancy = 'https://raw.githubusercontent.com/liu3388/maps_csv/main/rental_vacancy.csv'
df_vacancy = pd.read_csv(url_vacancy)


#%%set up path to save output map
os.chdir("C:\\Tai\\RE_project\\Github\\maps\\output")
path_csv = os.getcwd()


#%% select columns from both dfs
df_vacancy = df_vacancy.iloc[:,[0,-1]] #select most recent column
df_vacancy = df_vacancy[df_vacancy["3Q2022"].str.contains("(z)")==False] #drop rows with '(z)

df_MSA = df_MSA1[['NAME','geometry']] #select relevant columns from df_MSA

#merge df_vacancy and df_MSA
df_vacancy = df_vacancy.set_index('MSA')
df_vacancy = df_vacancy.astype(str).astype(float) #convert vacancy column data types from object to float
df_vacancy[qtr] = (df_vacancy[qtr] / 100).round(2)

df_MSA = df_MSA.set_index('NAME')
df = df_vacancy.join(df_MSA, how='outer')
df.dropna(inplace=True) 

df = df.reset_index()
df.rename({'index': 'MSA'}, axis=1, inplace=True)


#%% create base map for US
us_map = folium.Map(location=[37, -96], zoom_start=5,tiles='openstreetmap')

#%%
#Create the choropleth map add it to the base map
# custom_scale = (df[qtr].quantile((0,0.3,0.6,0.9,1))).tolist()

custom_scale = (df[qtr].quantile((0,0.25,0.5,0.75,1))).tolist()

folium.Choropleth(
            
            geo_data=r'C:\Tai\RE_project\Github\maps\GeoJson\maps_GeoJson\MSA.json',
            data=df,
            columns=['MSA', qtr],
            key_on='feature.properties.NAME',  #Here we grab the geometries/county boundaries from the geojson file using the key 'coty_code' which is the same as county fips
            threshold_scale=custom_scale, #use the custom scale we created for legend
            fill_color='YlOrRd',
            nan_fill_color="White", #Use white color if there is no data available for the county
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Rental vacancy rate', #title of the legend
            highlight=True,
            line_color='black'
            
            ).add_to(us_map)

#%%
#Add Customized Tooltips to the map
df_MSA_tooltip = df_MSA1
df_MSA_tooltip.set_index('NAME', inplace=True)
df_MSA_tooltip = df_MSA_tooltip.join(df_vacancy, how='outer')
df_MSA_tooltip.reset_index(inplace=True)

df_MSA_tooltip['3Q2022'] = df_MSA_tooltip['3Q2022'].transform(lambda x: '{:,.0%}'.format(x))

folium.features.GeoJson(
                    data=df_MSA_tooltip, #this needs to be a GeoJson file
                    
                    name=qtr,
                    smooth_factor=2,
                    style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['index',
                                qtr,
                                ],
                        aliases=['MSA:',
                                'Vacancy rate:',
                                  ], 
                        
                        localize=False,
                        sticky=True,
                        labels=True,
                        style="""
                            background-color: #F0EFEF;
                            border: 2px solid black;
                            border-radius: 3px;
                            box-shadow: 3px;
                            font-size: 14pt;
                        """,
                        max_width=800,),
                            highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                        ).add_to(us_map)

us_map
#%%

title_html = '''
             <h3 align="center" style="font-size:30px"><b>Rental Vacancy Rate for Select Metropolitan Statistical Areas (MSA), 3Q 2022</b></h3>
             '''
us_map.get_root().html.add_child(folium.Element(title_html))

#%%
us_map.save("mymap.html")



