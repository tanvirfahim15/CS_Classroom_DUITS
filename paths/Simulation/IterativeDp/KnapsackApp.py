import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, app, Blueprint
from Database.database import db
from pattern.SimulationStrategy.Context import SimulationContext

import classes.Simulation.IterativeDp.Knapsack as knpsck

app = Blueprint('knpsack', __name__)


@app.route("/idp/knapsack/entry", methods=['POST', 'GET'])
def knapsack_entry():
    return render_template(
        '/simulation/knapsack_iterative_dp/knapsack_iterative_dp_entry.html', **locals())


@app.route("/idp/knapsack/entry_data", methods=['POST', 'GET'])
def knapsack_entry_data():
    if request.method == 'POST':
        data = request.form
        data = {'knapsack_array1' : data['knapsack_array1'], 'knapsack_array2' : data['knapsack_array2'], 'knapsack_size' : data['knapsack_size']}
        posts = db.knapsack
        post_id = posts.insert_one(data).inserted_id
        return redirect('/idp/knapsack/' + str(post_id))
    return redirect('/idp/knapsack/entry')


@app.route('/idp/knapsack/<string:name>/')
def knapsack_simulation(name):
    data = db.knapsack.find_one({"_id": ObjectId(name)})

    array1 = ast.literal_eval(data['knapsack_array1'])
    arr_size1 = 0

    array2 = ast.literal_eval(data['knapsack_array2'])
    arr_size2 = 0
    knapsack_size = int(data['knapsack_size'])

    knapsack_array1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0 ,0 ,0,0,0,0]
    knapsack_array2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0 ,0 ,0,0,0,0]

    for i in range(len(array1)):
        knapsack_array1[i+1] = int(array1[i])
        arr_size1+=1

    for i in range(len(array2)):
        knapsack_array2[i+1] = int(array2[i])
        arr_size2+=1

    print(knapsack_array1)
    print(knapsack_array2)

    simulation_strategy = knpsck.KnapSack(int(knapsack_size), int(arr_size2), knapsack_array1, knapsack_array2)
    simulation_context = SimulationContext(simulation_strategy)
    data = simulation_context.get_data()
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "knapsack"})
        if key is not None:
            saved = 1
    return render_template(
        '/simulation/knapsack_iterative_dp/knapsack_iterative_dp_simulation.html', **locals())

