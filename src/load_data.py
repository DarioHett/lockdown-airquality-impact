'''
Loading the data from ../data/*

Data retrieved from https://www.hlnug.de/messwerte/luft/recherche-1

Files:
frdbrgr_170300_170320.txt 
hanau_170300_170320.txt 
ost_170300_170320.txt

@author: Dario Hett
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta

def load_data():
    ''' Loads the respective data. 
    
    Adjust files
    '''
    files = ["frdbrgr_170300_170320.txt", "hanau_170300_170320.txt", "ost_170300_170320.txt"]
    path = "../data/"

    header_dict = {'Benzol[µg/m³]' : 'benzol',
                   'Kohlenmonoxid (CO)[mg/m³]' : 'co',
                   'Kohlenwasserstoffe ohne Methan[mg/m³]' : 'carbhydros',
                   'Luftdruck[hPa]' : 'hpa',
                   'Methan[mg/m³]' : 'ch4',
                   'Ozon (O3)[µg/m³]' : 'o3',
                   'PM10[µg/m³]' : 'pm10',
                   'PM2,5[µg/m³]' : 'pm2.5',
                   'Relative Luftfeuchtigkeit[%]' : 'humidity',
                   'Schwefeldioxid (SO2)[µg/m³]' : 'so2',
                   'Staub[µg/m³]' : 'dust',
                   'Stickstoffdioxid (NO2)[µg/m³]' : 'no2',
                   'Stickstoffmonoxid (NO)[µg/m³]' : 'no',
                   'Temperatur[°C]' : 'temp',
                   'Toluol[µg/m³]' : 'toluol',
                   'Windgeschwindigkeit[m/s]' : 'windspeed',
                   'Windrichtung[Grad]' : 'winddirection',
                   'Datum' : 'date',
                   'Zeit' : 'time',
                   'm-/p-Xylol[µg/m³]' : 'xylol-mp',
                   'o-Xylol[µg/m³]' : 'xylol-o'}

    for file in files:
        new = pd.read_csv(path+file, sep=';', header='infer', skip_blank_lines=False, engine = 'python',
                          index_col=False, parse_dates = [0,1], dayfirst=True, decimal=',', thousands='.',
                          na_values = ['-'])
        new.rename(columns = header_dict,inplace=True)
        try:
            frames.append(new)
            loc.append(file)
        except: 
            frames = [new]
            loc = [file]
            
    df = pd.concat(frames, axis=0, join='outer', ignore_index=False, keys=loc,
                   levels=None, names=None, verify_integrity=False, copy=False)      

    df = df.droplevel(1,axis=0)

    assert(len(df.columns) == len(header_dict)) # Header dict was constructred from the unions.
    del new, file

    # Set types.
    df[df.columns[2:]].astype('float', copy=False)

    df.loc[df.time == "24:00",'date'] = df.loc[df.time == "24:00",'date'] + timedelta(days=1)
    df.loc[df.time == "24:00",'time'] = "00:00"
    df['time'] = pd.to_timedelta(df.time+':00', unit='H')
    df['date'] = pd.to_datetime(df.date, format="%Y-%m-%d")
    df['datetime'] = df['time']+df['date']

    return df, files, header_dict