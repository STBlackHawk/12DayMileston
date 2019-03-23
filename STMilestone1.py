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
from bokeh.plotting import figure, output_file, show
from flask import Flask,render_template,request,redirect
import datetime









app_STMilestone = Flask(__name__)

prTypes=[]
colors = ["navy", "green", "purple", "red"]
prType = ["Adj_Open","Adj_High", "Adj_Low", "Adj_Close"]
#cmdict={}
#cmdict["Home Depot"] = "HD"
#cmdict["The Walt Disney Company"] = "DIS"
#cmdict["Microsoft Corporation"]="MSFT"
#cmdict["The Boeing Company"]="BA" 
#
#
#prType={}
#prType["Adjusted Open"] = "Adj_Open"
#prType["Adjusted High"] = "Adj_High"
#prType["Adjusted Low"] = "Adj_Low"
#prType["Adjusted Closing"] = "Adj_Close"



@app_STMilestone.route('/index',methods=['GET','POST'])
def index_lulu():
    if request.method == 'GET':
        return render_template('Page1.html')
    else:
        Company = request.form["Company"]
        stDate = request.form["stdate"]
        endDate = request.form["enddate"]
        
        
        for i in prType:
            if request.form.__contains__("Adj_Low"):
                prTypes.append(request.form[i])
        
#        app_STMilestone.prTypes.append(request.form["Adj_Open"])
#        app_STMilestone.prTypes.append(request.form["Adj_High"])
#        app_STMilestone.prTypes.append(request.form["Adj_Low"])
#        app_STMilestone.prTypes.append(request.form["Adj_Close"])
        
        
        
        stDate = datetime.datetime.strptime(stDate,"%Y-%m-%d").strftime("%Y-%m-%d")
        endDate = datetime.datetime.strptime(endDate,"%Y-%m-%d").strftime("%Y-%m-%d")

        if stDate > endDate :
            return redirect("/error")
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
            
            return redirect("/plot")
        

@app_STMilestone.route("/plot")
def plot():
    return render_template("stocks.html")


@app_STMilestone.route("/error", methods=["GET","POST"])
def error():
    if request.method == "GET":
        return render_template("error.html")
    else:
        return render_template("Page1.html")


if __name__ == "__main__":
    app_STMilestone.run(debug=True)
