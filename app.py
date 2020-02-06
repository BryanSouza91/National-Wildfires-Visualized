import numpy as np
import os
from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
from dtime import is_leap_year, ymd


# Setup Flask 

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Project_2_db"
mongo = PyMongo(app)

# This is where we put functions to filter and sort
fires_2004 = mongo.db.fires.find({"FIRE_YEAR": 2004})
dates_2004 = []
for v in fires_2004:
    yr = v['FIRE_YEAR']
    dy = v['DISCOVERY_DOY']
    dates_2004.append(ymd(yr,dy))


# Define Flask Routes
@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/table")
def table_page():
    return render_template("table.html",
        dates_2004=dates_2004)





if __name__ == '__main__':
    app.run(debug=True)
