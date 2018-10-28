import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, app, Blueprint
from Database.database import db
import classes.Simulation.IterativeDp.EditDistance as edis
from pattern.SimulationStrategy.Context import SimulationContext

app = Blueprint('edit_distance', __name__)


@app.route("/idp/edit-distance/entry", methods=['POST', 'GET'])
def edit_distance_entry():
    return render_template(
        '/simulation/edit_distance_iterative_dp/edit_distance_iterative_dp_entry.html', **locals())


@app.route("/idp/edit-distance/entry_data", methods=['POST', 'GET'])
def edit_distance_entry_data():
    if request.method == 'POST':
        data = request.form
        data = {'string1': data['string1'], 'string2': data['string2']}
        posts = db.edit_distance
        post_id = posts.insert_one(data).inserted_id
        return redirect('/idp/edit-distance/' + str(post_id))
    return redirect('/idp/edit-distance/entry')


@app.route('/idp/edit-distance/<string:name>/')
def edit_distance_simulation(name):
    data = db.edit_distance.find_one({"_id": ObjectId(name)})

    print(data['string1'])

    simulation_strategy = edis.EditDistance(data['string1'], data['string2'])
    simulation_context = SimulationContext(simulation_strategy)
    data = simulation_context.get_data()

    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "edit_distance"})
        if key is not None:
            saved = 1
    return render_template(
        '/simulation/edit_distance_iterative_dp/edit_distance_iterative_dp_simulation.html', **locals())