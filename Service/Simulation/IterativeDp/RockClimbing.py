import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from Database.database import db
from classes.Simulation.IterativeDp import RockClimbing as rc
from pattern.SimulationStrategy.Context import SimulationContext


def rock_climbing_entry_data(data):
    data = {'string1' : data['string1'],'string2' : data['string2']}
    posts = db.rock_climbing
    post_id = posts.insert_one(data).inserted_id
    return post_id


def rock_climbing_simulation(name):
    data = db.rock_climbing.find_one({"_id": ObjectId(name)})

    dp_simulation_strategy = rc.RockClimbing(data['string1'], data['string2'])
    dp_simulation_context = SimulationContext(dp_simulation_strategy)
    data = dp_simulation_context.get_data()

    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "lcs"})
        if key is not None:
            saved = 1
    return data, saved