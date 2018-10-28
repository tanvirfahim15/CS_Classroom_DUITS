import ast

from bson import ObjectId
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, session, app, Blueprint
import classes.Calculator.StatisticsStd as stdev
from Database.database import db

app = Blueprint('box_plot', __name__)

@app.route("/calc/stat/boxplot/entry", methods=['POST', 'GET'])
def stat_entry():
    return render_template(
        '/calculator/statistical/box_plot_entry.html', **locals())


@app.route("/calc/stat/boxplot/entry_data", methods=['POST', 'GET'])
def stat_entry_data():
    if request.method == 'POST':
        data = request.form
        data = {'stat_array' : data['stat_array']}
        posts = db.stat
        post_id = posts.insert_one(data).inserted_id
        return redirect('/calc/stat/boxplot/' + str(post_id))
    return redirect('/calc/stat/boxplot/entry_data')


@app.route('/calc/stat/boxplot/<string:name>/')
def stat_simulation(name):
    data = db.stat.find_one({"_id": ObjectId(name)})
    arr = ast.literal_eval(data['stat_array'])
    arr_size = 0
    stat_array = []

    # [9 , 2 , 5 , 3 , 7 , 11, 8, 7, 3]

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
                                            "algo": "BoxPlot"})
        if key is not None:
            saved = 1
    return render_template(
        '/calculator/statistical/box_plot.html', **locals())