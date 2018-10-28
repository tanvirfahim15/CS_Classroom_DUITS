from bson import ObjectId
from flask import render_template, request, redirect, session, app, Blueprint
from Database.database import db
from classes.Simulation.IterativeDp.LCS import LCS
from pattern.SimulationStrategy.Context import SimulationContext


def longest_common_subsequence():
    name = '5bd118b776cc9d2f4663873f'
    data = db.longest_common_subsequence.find_one({"_id": ObjectId(name)})

    simulation_strategy = LCS(data['string1'], data['string2'])
    simulation_context = SimulationContext(simulation_strategy)

    data = simulation_context.get_data()
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "lcs"})
        if key is not None:
            saved = 1
    return data, saved


def longest_common_subsequence_entry_data(data):
    data = {'string1': data['string1'], 'string2': data['string2']}
    print(data)
    posts = db.longest_common_subsequence
    post_id = posts.insert_one(data).inserted_id
    return post_id


def longest_common_subsequence_simulation(name):
    data = db.longest_common_subsequence.find_one({"_id": ObjectId(name)})

    simulation_strategy = LCS(data['string1'], data['string2'])
    simulation_context = SimulationContext(simulation_strategy)

    data = simulation_context.get_data()
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "lcs"})
        if key is not None:
            saved = 1
    return data, saved
