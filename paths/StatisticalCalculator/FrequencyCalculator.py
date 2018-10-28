import ast

from bson import ObjectId
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, session, app, Blueprint
import classes.Calculator.statistics as stat
from Database.database import db

app = Blueprint('freq_calc', __name__)

@app.route("/calc/stat/freq/entry", methods=['POST', 'GET'])
def stat_freq_entry():
    return render_template(
        '/calculator/statistical/stat_entry_freq.html', **locals())


@app.route("/calc/stat/freq/entry_data", methods=['POST', 'GET'])
def stat_freq_entry_data():
    if request.method == 'POST':
        data = request.form
        data = {'stat_array' : data['stat_array']}
        posts = db.stat
        post_id = posts.insert_one(data).inserted_id
        return redirect('/calc/stat/freq/' + str(post_id))
    return redirect('/calc/stat/freq/entry_data')


@app.route('/calc/stat/freq/<string:name>/')
def stat_freq_simulation(name):
    data = db.stat.find_one({"_id": ObjectId(name)})
    arr = ast.literal_eval(data['stat_array'])
    arr_size = 0
    stat_array = []

    for i in range(len(arr)):
        stat_array.append(0)

    for i in range(len(arr)):
        stat_array[i] = int(arr[i])
        arr_size += 1

    s_temp = stat.statistics(int(arr_size), stat_array)
    data = s_temp.get_data()
    # 26,30,45,89,89,74,54,74,26,30,30,26,78,89,54,56,14,54,14
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "Statistics",
                                            "algo": "Frequency"})
        if key is not None:
            saved = 1
    return render_template(
        '/calculator/statistical/stat_output.html', **locals())