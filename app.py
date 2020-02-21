import numpy as np
import pandas as pd
import os
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import json

# Setup Flask
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Project_2_db"
mongo = PyMongo(app)

# Define Flask Routes
@app.route("/", methods=["GET"])
def home_page():
    if request.method == "GET":
        states_df = pd.DataFrame.from_records(
            mongo.db.fires.find({"FIRE_SIZE": { "$gte": 1000 }}, {"STATE": 1}).limit(10000))
        state_list = []
        state_list = [state for state in states_df.STATE.sort_values(
            ascending=True).unique()]
        return render_template("index.html", data={"states": state_list})

# get data function
# create list of lists for highcharts
@app.route("/api/<state0>", methods=["GET"])
def get_data(state0):

    # pulls in data based on api state variable
    df0 = pd.DataFrame.from_records(mongo.db.fires.find(
        {"STATE": state0, "FIRE_SIZE": { "$gte": 1000 }}, {"STAT_CAUSE_DESCR": 1, 'FIRE_SIZE': 1, 'FIRE_YEAR': 1, 'DAYS_TO_CONT': 1}))   # {"$gte": 10 }

    # build pivot table for fire size
    cause_size_pivot = pd.pivot_table(df0, values='FIRE_SIZE', index=['FIRE_YEAR'],
                                      columns=['STAT_CAUSE_DESCR'], aggfunc=np.sum, fill_value=0)

    # structure data from pivot for streamgraph
    years_categories = [str(x) for x in cause_size_pivot.index]
    streamgraph_data = []
    for each in cause_size_pivot.iteritems():
        each_cause = {
            "name": each[0],
            "data": [round(v, 2) for k, v in cause_size_pivot[each[0]].items()]
        }
        streamgraph_data.append(each_cause)

    # structure data from pivot for variable pie
    vpie_size_df = pd.DataFrame(df0.groupby(
        ['STAT_CAUSE_DESCR']).FIRE_SIZE.sum())
    vpie_count_df = pd.DataFrame(df0.STAT_CAUSE_DESCR.value_counts())
    vpie__df = vpie_size_df.merge(
        vpie_count_df, left_index=True, right_index=True)
    vpie_data = []
    for each in vpie__df.iterrows():
        each_slice = {
            "name": each[0],
            "y": round(each[1].FIRE_SIZE, 2),
            "z": round(each[1].STAT_CAUSE_DESCR)
        }
        vpie_data.append(each_slice)

    # line chart
    cont_pivot = pd.pivot_table(df0, values='DAYS_TO_CONT', columns=['FIRE_YEAR'],
                                index=['STAT_CAUSE_DESCR'], aggfunc=np.sum, fill_value=0)
    size_pivot = pd.pivot_table(df0, values='FIRE_SIZE', columns=['FIRE_YEAR'],
                                index=['STAT_CAUSE_DESCR'], aggfunc=np.sum, fill_value=0)
    cont_list = []
    for index, group in cont_pivot.iterrows():
        years = [str(index_) for index_, item in group.iteritems()]
        nums = [item for index_, item in group.iteritems()]
        data = [[str(index_),item] for index_,item in group.iteritems()]
        each_cause = {
            "cause": index,
            "data": {
                "years": years,
                "cont_data": nums,
                "drilldown": data}
        }
        cont_list.append(each_cause)
    size_list = []
    for index, group in size_pivot.iterrows():
        years = [str(index_) for index_, item in group.iteritems()]
        nums = [item for index_, item in group.iteritems()]
        each_cause = {
            "cause": index,
            "data": {
                "years": years,
                "size_data": nums}
        }
        size_list.append(each_cause)

    # put into data variable for json
    data = {
        "column": {
            "counts": [[k, v] for k, v in df0.STAT_CAUSE_DESCR.value_counts().items()],
            "days_to_cont": cont_list,
            "sizes": size_list},
        "v_pie": vpie_data,
        "streamGraph": {
            "data": streamgraph_data,
            "years_categories": years_categories},

    }
    return data


if __name__ == '__main__':
    app.run(debug=True)
