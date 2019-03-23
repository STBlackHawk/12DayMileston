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
from flask import Flask,render_template,request,redirect, session
import datetime







app_STMilestone = Flask(__name__)



app_STMilestone.prTypes=[]
colors = ["navy", "green", "purple", "red"]
prTypes = ["Adj_Open","Adj_High", "Adj_Low", "Adj_Close"]
cmdict={}
cmdict["HD"] = "Home Depot"
cmdict["DIS"] = "The Walt Disney Company"
cmdict["MSFT"]="Microsoft Corporation"
cmdict["BA"]="The Boeing Company" 
#
#
#prType={}
#prType["Adjusted Open"] = "Adj_Open"
#prType["Adjusted High"] = "Adj_High"
#prType["Adjusted Low"] = "Adj_Low"
#prType["Adjusted Closing"] = "Adj_Close"



@app_STMilestone.route("/",methods=["GET","POST"])
def index_lulu():
    j=0
    if request.method == "GET":
        return render_template("Page1.html")
        session.clear()
    else:
        app_STMilestone.Company = request.form["Company"]
        app_STMilestone.stDate = request.form["stdate"]
        app_STMilestone.endDate = request.form["enddate"]
        
        
        for i in prTypes:
            if request.form.__contains__(i):
                app_STMilestone.prTypes.append(request.form[i])
        
#        app_STMilestone.prTypes.append(request.form["Adj_Open"])
#        app_STMilestone.prTypes.append(request.form["Adj_High"])
#        app_STMilestone.prTypes.append(request.form["Adj_Low"])
#        app_STMilestone.prTypes.append(request.form["Adj_Close"])
        
        
        
        stDate = datetime.datetime.strptime(app_STMilestone.stDate,"%Y-%m-%d").strftime("%Y-%m-%d")
        endDate = datetime.datetime.strptime(app_STMilestone.endDate,"%Y-%m-%d").strftime("%Y-%m-%d")

        if stDate > endDate :
            return redirect("/error")
        else:
            r = requests.get("https://www.quandl.com/api/v3/datasets/EOD/"+app_STMilestone.Company+"?start_date="+app_STMilestone.stDate+"&end_date="+app_STMilestone.endDate+"&api_key=eyATCrv5WpEWyhfUJ_Ge")
            data =r.json() 
            db = pd.DataFrame(data["dataset"]["data"], columns=data["dataset"]["column_names"])
            
            stocks={}
            
            # prepare some data
            for i in app_STMilestone.prTypes:
                stocks[i] = np.array(db[i])
            
            
            dates = np.array(db['Date'], dtype=np.datetime64)
            
            
            
            # output to static HTML file
            output_file("templates/stocks.html", title="stocks.py example")
            
            # create a new plot with a a datetime axis type
            p = figure(plot_width=800, plot_height=350, x_axis_type="datetime")
            
            # add renderers
            
            for i in app_STMilestone.prTypes:
                p.line(dates, stocks[i], color=colors[j], legend=i)
                j+=1
            
            # NEW: customize by setting attributes
            p.title.text = cmdict[app_STMilestone.Company]+" stock prices From "+app_STMilestone.stDate +" to "+app_STMilestone.endDate 
            p.legend.location = "top_left"
            p.grid.grid_line_alpha = 0
            p.xaxis.axis_label = 'Date'
            p.yaxis.axis_label = 'Price'
            p.ygrid.band_fill_color = "olive"
            p.ygrid.band_fill_alpha = 0.1
            save(p)
            
            return redirect("/plot")
            session.clear()
        

@app_STMilestone.route("/plot")
def plot():
    return render_template("stocks.html")


@app_STMilestone.route("/error", methods=["GET","POST"])
def error():
    if request.method == "GET":
        return render_template("error.html")
    else:
        session.clear()
        return redirect("/")
        


if __name__ == "__main__":
    app_STMilestone.run(debug=True)
