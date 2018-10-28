import  ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from Database.database import db
from classes.Simulation.IterativeDp import SCS as scs
from pattern.SimulationStrategy.Context import SimulationContext


def shortest_common_supersequence_entry_data(data):
    data = {'string1' : data['string1'],'string2' : data['string2']}
    posts = db.shortest_common_supersequence
    post_id = posts.insert_one(data).inserted_id
    return post_id


def shortest_common_supersequence_simulation(name):
    data = db.shortest_common_supersequence.find_one({"_id": ObjectId(name)})

    dp_simulation_strategy = scs.SCS(data['string1'], data['string2'])
    dp_simulation_context = SimulationContext(dp_simulation_strategy)
    data = dp_simulation_context.get_data()

    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "lcs"})
        if key is not None:
            saved = 1
    return data, saved