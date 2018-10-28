import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, app, Blueprint
from Database.database import db
from pattern.SimulationStrategy.Context import SimulationContext

import classes.Simulation.IterativeDp.LIS as lis

app = Blueprint('lis', __name__)

@app.route("/idp/longest-increasing-subsequence/entry", methods=['POST', 'GET'])
def longest_increasing_subsequence_entry():
    return render_template(
        '/simulation/lis_iterative_dp/lis_iterative_dp_entry.html', **locals())


@app.route("/idp/longest-increasing-subsequence/entry_data", methods=['POST', 'GET'])
def longest_increasing_subsequence_entry_data():
    if request.method == 'POST':
        data = request.form
        data = {'lis_array' : data['lis_array']}
        posts = db.longest_increasing_subsequence
        post_id = posts.insert_one(data).inserted_id
        return redirect('/idp/longest-increasing-subsequence/' + str(post_id))
    return redirect('/idp/longest-increasing-subsequence/entry')


@app.route('/idp/longest-increasing-subsequence/<string:name>/')
def longest_increasing_subsequence_simulation(name):
    data = db.longest_increasing_subsequence.find_one({"_id": ObjectId(name)})
    #arr = data['lis_array']
    arr = ast.literal_eval(data['lis_array'])
    arr_size = 0
    lis_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0 ,0 ,0,0,0,0]
    for i in range(len(arr)):
        lis_array[i+1] = int(arr[i])
        arr_size+=1

    simulation_strategy = lis.LIS(int(arr_size), lis_array)
    simulation_context = SimulationContext(simulation_strategy)
    data = simulation_context.get_data()
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "lis"})
        if key is not None:
            saved = 1
    return render_template(
        '/simulation/lis_iterative_dp/lis_iterative_dp_simulation.html', **locals())