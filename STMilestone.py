#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 18:21:11 2019

@author: blackhawk
"""
import numpy as np
import requests
import simplejson as json
import pandas as pd
from pandas.io.json import json_normalize 
from bokeh.plotting import figure, output_file, show, save
from flask import Flask,render_template,request,redirect, session, Request
import datetime



app_STMilestone = Flask(__name__)



colors = ["navy", "green", "purple", "red"]
prTypes = ["Adj_Open","Adj_High", "Adj_Low", "Adj_Close"]
cmdict={}
cmdict["HD"] = "Home Depot"
cmdict["DIS"] = "The Walt Disney Company"
cmdict["MSFT"]="Microsoft Corporation"
cmdict["BA"]="The Boeing Company" 




@app_STMilestone.route("/",methods=["GET","POST"])
def index_lulu():
    app_STMilestone.prTypes=[]
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
            r = requests.get("https://www.quandl.com/api/v3/datasets/EOD/"+Company+"?start_date="+stDate+"&end_date="+endDate+"&api_key=eyATCrv5WpEWyhfUJ_Ge")
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
          

@app_STMilestone.route("/plot")
#def plot():
#    return render_template("stocks.html")


@app_STMilestone.route("/error", methods=["GET","POST"])
def error():
    if request.method == "GET":
        return render_template("error.html")
    else:
        return redirect("/")
        


if __name__ == "__main__":
    app_STMilestone.run(debug=False)
