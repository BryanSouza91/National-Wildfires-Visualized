import numpy as np
import os
from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
from dtime import is_leap_year, ymd
import pandas as pd


# Setup Flask 

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Project_2_db"
mongo = PyMongo(app)


# Define Flask Routes
@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/table/<state0>/<state1>")
def table_page(state0,state1):
    df0 = pd.DataFrame.from_records(mongo.db.fires.find({"STATE": state0 }))
    df1 = pd.DataFrame.from_records(mongo.db.fires.find({"STATE": state1 }))
    return render_template("table.html", data={
                                            "state": (state0,state1),
                                            "causes": {
                                                "state0": df0.STAT_CAUSE_DESCR.value_counts(),
                                                "state1": df1.STAT_CAUSE_DESCR.value_counts()
                                                }
                                            })



if __name__ == '__main__':
    app.run(debug=True)
