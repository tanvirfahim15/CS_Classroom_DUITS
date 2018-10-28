from flask import render_template, request, redirect, session, app, Blueprint
from Database.database import db
from classes.Simulation.LinearAlgebra.GaussElimination import GaussElimination as gs
import classes.Simulation.LinearAlgebra.GaussElimination.Utility as gs_util
from bson import ObjectId
import json
from pattern.SimulationStrategy.Context import SimulationContext


def gauss_elimination():
    name = '5bd208bb76cc9d1287c8941e'
    data = db.gauss_elimination.find_one({"_id": ObjectId(name)})
    data = str(data)
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "la",
                                            "algo": "gs"})
        if key is not None:
            saved = 1
    return data, saved, name


def gauss_elimination_simulation(name):
    data = db.gauss_elimination.find_one({"_id": ObjectId(name)})
    data = str(data)
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "la",
                                            "algo": "gs"})
        if key is not None:
            saved = 1
    return data, saved


def gauss_elimination_data(name):
    data = db.gauss_elimination.find_one({"_id": ObjectId(name)})
    data = [data['matrices'], data['records']]
    data = str(data)
    return data


def gauss_elimination_entry_data(data):
    data = str(json.dumps(data['entry']))
    if gs_util.validate_entry(data) is False:
        return False, data.replace('\"', '').replace('\\r\\n', '\n')
    else:
        mat = gs_util.get_matrix(data)

        simulation_strategy = gs.GaussElimination(mat)
        simulation_context = SimulationContext(simulation_strategy)
        data = simulation_context.get_data()

        posts = db.gauss_elimination
        post_id = posts.insert_one(data).inserted_id
        return True, str(post_id)
