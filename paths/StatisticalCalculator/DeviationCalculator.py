import ast

from bson import ObjectId
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, session, app, Blueprint
import classes.Calculator.StatisticsStd as stdev
from Database.database import db

app = Blueprint('dev_calc', __name__)

@app.route("/calc/stat/entry", methods=['POST', 'GET'])
def stat_entry():
    return render_template(
        '/calculator/statistical/stat_entry.html', **locals())


@app.route("/calc/stat/entry_data", methods=['POST', 'GET'])
def stat_entry_data():
    if request.method == 'POST':
        data = request.form
        data = {'stat_array' : data['stat_array']}
        posts = db.stat
        post_id = posts.insert_one(data).inserted_id
        return redirect('/calc/stat/' + str(post_id))
    return redirect('/calc/stat/entry_data')


@app.route('/calc/stat/<string:name>/')
def stat_simulation(name):
    data = db.stat.find_one({"_id": ObjectId(name)})
    arr = ast.literal_eval(data['stat_array'])
    arr_size = 0
    stat_array = []

    # 5, 12, 6, 8 , 14

    for i in range(100):
        stat_array.append(0)

    for i in range(len(arr)):
        stat_array[i] = int(arr[i])
        arr_size += 1

    s_temp = stdev.Statistics(int(arr_size), stat_array)
    data = s_temp.get_data()

    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "Statistics",
                                            "algo": "Unordered"})
        if key is not None:
            saved = 1
    return render_template(
        '/calculator/statistical/stat_output_stddev.html', **locals())