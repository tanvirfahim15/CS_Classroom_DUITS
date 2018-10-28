from flask import render_template, request, redirect, session, app, Blueprint
from Database.database import db
import json
from classes.Simulation.LinearAlgebra.GaussJordanElimination import GaussJordanElimination as gj
import classes.Simulation.LinearAlgebra.GaussJordanElimination.Utility as gj_util
from bson import ObjectId
from pattern.SimulationStrategy.Context import SimulationContext


def gauss_jordan_elimination():
    name = '5bd21b6f76cc9d164673acf5'
    data = db.gauss_jordan_elimination.find_one({"_id": ObjectId(name)})
    data = str(data)
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "la",
                                            "algo": "gj"})
        if key is not None:
            saved = 1
    return name, data, saved


def gauss_jordan_elimination_simulation(name):
    data = db.gauss_jordan_elimination.find_one({"_id": ObjectId(name)})
    data = str(data)
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "la",
                                            "algo": "gj"})
        if key is not None:
            saved = 1
    return data, saved


def gauss_jordan_elimination_data(name):
    data = db.gauss_jordan_elimination.find_one({"_id": ObjectId(name)})
    data = [data['matrices'], data['records']]
    data = str(data)
    return data


def gauss_jordan_elimination_entry_data(data):
    data = str(json.dumps(data['entry']))
    if gj_util.validate_entry(data) is False:
        return False, data.replace('\"', '').replace('\\r\\n', '\n')
    else:
        mat = gj_util.get_matrix(data)

        simulation_strategy = gj.GaussJordanElimination(mat)
        simulation_context = SimulationContext(simulation_strategy)
        data = simulation_context.get_data()

        posts = db.gauss_jordan_elimination
        post_id = posts.insert_one(data).inserted_id
        return True, str(post_id)
