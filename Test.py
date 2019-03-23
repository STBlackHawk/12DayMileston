#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 12:27:55 2019

@author: blackhawk
"""

import numpy as np
import requests
import simplejson as json
import pandas as pd
from pandas.io.json import json_normalize 
from bokeh.plotting import figure, output_file, show
import datetime

colors = ["navy", "green", "purple", "red"]
prTypes = ["Adj_Open","Adj_High", "Adj_Low", "Adj_Close"]

stDate="2018-01-01"
endDate="2019-01-01"
Company = "HD"

stDate = datetime.datetime.strptime(stDate,"%Y-%m-%d").strftime("%Y-%m-%d")
endDate = datetime.datetime.strptime(endDate,"%Y-%m-%d").strftime("%Y-%m-%d")

if stDate > endDate :
     print("Uncompatible dates")
else:
    r = requests.get("https://www.quandl.com/api/v3/datasets/EOD/"+Company+"?start_date="+stDate+"&end_date="+endDate+"&api_key=eyATCrv5WpEWyhfUJ_Ge")
    data =r.json() 
    db = pd.DataFrame(data["dataset"]["data"], columns=data["dataset"]["column_names"])
    
    stocks={}
    
    # prepare some data
    for i in prTypes:
        stocks[i] = np.array(db[i])
    
    
    dates = np.array(db['Date'], dtype=np.datetime64)
    
    
    
    # output to static HTML file
    output_file("templates/stocks.html", title="stocks.py example")
    
    # create a new plot with a a datetime axis type
    p = figure(plot_width=800, plot_height=350, x_axis_type="datetime")
    
    # add renderers
    j=0
    for i in prTypes:
        p.line(dates, stocks[i], color=colors[j], legend=i)
        j+=1
    
    # NEW: customize by setting attributes
    p.title.text = Company+" stock prices From "+stDate +" to "+endDate 
    p.legend.location = "top_left"
    p.grid.grid_line_alpha = 0
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.ygrid.band_fill_color = "olive"
    p.ygrid.band_fill_alpha = 0.1
    show(p)