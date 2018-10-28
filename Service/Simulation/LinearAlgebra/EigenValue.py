from flask import render_template, request, redirect, session, app, Blueprint
from Database.database import db
from bson import ObjectId
import json
from classes.Simulation.LinearAlgebra.EigenValue import Utility as eigen_util
from classes.Simulation.LinearAlgebra.EigenValue import EigenValue as eigen
from pattern.SimulationStrategy.Context import SimulationContext


def eigen_value():
    name = "5bd22ecf76cc9d20a507c41f"
    data = db.eigen_value.find_one({"_id": ObjectId(name)})
    data.pop('_id')
    data = json.dumps(data)

    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "la",
                                            "algo": "ev"})
        if key is not None:
            saved = 1
    return name, data, saved


def eigen_value_simulation(name):
    data = db.eigen_value.find_one({"_id": ObjectId(name)})
    data.pop('_id')
    data = json.dumps(data)

    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "la",
                                            "algo": "ev"})
        if key is not None:
            saved = 1
    return data, saved


def eigen_value_entry_data(data):
    data = str(json.dumps(data['entry']))
    if eigen_util.validate_entry(data) is False:
        return False, data.replace('\"', '').replace('\\r\\n', '\n')
    else:

        simulation_strategy = eigen.EigenValue(eigen_util.get_matrix(data))
        simulation_context = SimulationContext(simulation_strategy)
        data = simulation_context.get_data()

        posts = db.eigen_value
        post_id = posts.insert_one(data).inserted_id
        return True, str(post_id)

