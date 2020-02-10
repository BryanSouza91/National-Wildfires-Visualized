import numpy as np
import os
from flask import Flask, jsonify, render_template, request
from flask_pymongo import PyMongo
from dtime import is_leap_year, ymd
import pandas as pd


# Setup Flask 

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Project_2_db"
mongo = PyMongo(app)


# Define Flask Routes
@app.route("/",methods=["GET","POST"])
def home_page():
    if request.method == "GET":
        states = pd.DataFrame.from_records(mongo.db.fires.find({},{"STATE": 1}).limit(10000))
        state_list = []
        state_list = [state for state in states.STATE.unique()]
        return render_template("index.html", data={"states": state_list})
    if request.method == "POST":
        states = pd.DataFrame.from_records(mongo.db.fires.find({},{"STATE": 1}).limit(10000))
        state_list = []
        state_list = [state for state in states.STATE.unique()]
        state0 = request.form.get('state0')
        state1 = request.form.get('state1')
        df0 = pd.DataFrame.from_records(mongo.db.fires.find({"STATE": state0 },{"STAT_CAUSE_DESCR": 1}))
        df1 = pd.DataFrame.from_records(mongo.db.fires.find({"STATE": state1 },{"STAT_CAUSE_DESCR": 1}))
        return render_template("table.html", data={
                                                "states": state_list,
                                                "state": (state0,state1),
                                                "causes": {
                                                    "state0": df0.STAT_CAUSE_DESCR.value_counts(),
                                                    "state1": df1.STAT_CAUSE_DESCR.value_counts()
                                                    }
                                                })

# @app.route("/",methods=["POST"])
# def table():
#     state0 = request.form.get('state0')
#     state1 = request.form.get('state1')
#     df0 = pd.DataFrame.from_records(mongo.db.fires.find({"STATE": state0 },{"STAT_CAUSE_DESCR": 1}))
#     df1 = pd.DataFrame.from_records(mongo.db.fires.find({"STATE": state1 },{"STAT_CAUSE_DESCR": 1}))
#     return render_template("table.html", data={
#                                             "state": (state0,state1),
#                                             "causes": {
#                                                 "state0": df0.STAT_CAUSE_DESCR.value_counts(),
#                                                 "state1": df1.STAT_CAUSE_DESCR.value_counts()
#                                                 }
#                                             })



if __name__ == '__main__':
    app.run(debug=True)
