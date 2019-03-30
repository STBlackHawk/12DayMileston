#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 18:21:11 2019

@author: blackhawk
"""
import os
import numpy as np
import requests

import pandas as pd
from bokeh.plotting import figure, output_file, save
from flask import Flask,render_template,request,redirect
import datetime



app_STMilestone = Flask(__name__)



colors = ["navy", "green", "purple", "red"]
prTypes = ["Adj_Open","Adj_High", "Adj_Low", "Adj_Close"]
cmdict={}
cmdict["HD"] = "Home Depot"
cmdict["DIS"] = "The Walt Disney Company"
cmdict["MSFT"]="Microsoft Corporation"
cmdict["BA"]="The Boeing Company" 

os.environ["API.i"] = "https://www.quandl.com/api/v3/datasets/EOD/"
os.environ["API.ii"] = "?start_date="
os.environ["API.iii"] = "&end_date="
os.environ["API.iv"] = "&api_key=eyATCrv5WpEWyhfUJ_Ge"



@app_STMilestone.route("/",methods=["GET","POST"])
def index_lulu():
    stocks ={}
    prtype =[]
    if request.method == "GET":
            
        return render_template("Page1.html")

    else:
        Company = request.form.get("Company")
        stDate = request.form.get("stdate")
        endDate = request.form.get("enddate")
        
        
        for i in prTypes:
            if request.form.__contains__(i):
                prtype.append(request.form.get(i))
        

        
        
        
        stDate = datetime.datetime.strptime(stDate,"%Y-%m-%d").strftime("%Y-%m-%d")
        endDate = datetime.datetime.strptime(endDate,"%Y-%m-%d").strftime("%Y-%m-%d")

        if stDate >= endDate :
            return redirect("/error")
        else:
            r = requests.get(os.environ["API.i"]+Company+os.environ["API.ii"]+stDate+os.environ["API.iii"]+endDate+os.environ["API.iv"])
            data =r.json() 
            db = pd.DataFrame(data["dataset"]["data"], columns=data["dataset"]["column_names"])
            
            
            # prepare some data
            for i in prtype:
                stocks[i] = np.array(db[i])
            
            
            dates = np.array(db['Date'], dtype=np.datetime64)
            
            
            
            # output to static HTML file
            output_file("templates/stocks.html", title="stocks")
            
            # create a new plot with a a datetime axis type
            p = figure(plot_width=800, plot_height=350, x_axis_type="datetime")
            
            # add renderers
            j=0
            for i in prtype:
                if j > 3 : 
                    j = 0
                p.line(dates, stocks[i], color=colors[j], legend=i)
                j+=1
            
            # NEW: customize by setting attributes
            p.title.text = cmdict[Company]+" stock prices From "+stDate +" to "+endDate 
            p.legend.location = "top_left"
            p.grid.grid_line_alpha = 0
            p.xaxis.axis_label = 'Date'
            p.yaxis.axis_label = 'Price'
            p.ygrid.band_fill_color = "olive"
            p.ygrid.band_fill_alpha = 0.1
            save(p)
            return render_template("stocks.html")

          

@app_STMilestone.route("/bokeh")
def plot():
    return render_template("stocks.html")



@app_STMilestone.route("/error", methods=["GET","POST"])
def error():
    if request.method == "GET":
        return render_template("error.html")
    else:
        return redirect("/")
        


if __name__ == "__main__":
    app_STMilestone.run(debug=False)
