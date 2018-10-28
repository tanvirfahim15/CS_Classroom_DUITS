import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from Database.database import db
from classes.Simulation.IterativeDp import MatrixChainMultiplication as mcm
from pattern.SimulationStrategy.Context import SimulationContext


def matrix_chain_multiplication_data_entry(data):
    data = {'dimension_array' : data['dimension_array']}
    posts = db.matrix_chain_multiplication
    post_id = posts.insert_one(data).inserted_id
    return post_id


def matrix_chain_multiplication_simulation(name):
    data = db.matrix_chain_multiplication.find_one({"_id": ObjectId(name)})
    dimensions = ast.literal_eval(data['dimension_array'])

    k = len(dimensions)

    dp_simulation_strategy = mcm.MatrixChainMultiplication(k, dimensions)
    dp_simulation_context = SimulationContext(dp_simulation_strategy)
    data = dp_simulation_context.get_data()

    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "matrix_chain_multiplication"})
        if key is not None:
            saved = 1
    return data, saved