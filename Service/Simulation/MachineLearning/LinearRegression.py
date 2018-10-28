import json
import numpy as np
from flask import render_template, request, redirect, session, Blueprint
from Database.database import db
from bson.objectid import ObjectId
from classes.Simulation.MachineLearning.LinearRegression import LinearRegression as lr
import classes.Simulation.MachineLearning.LinearRegression.Utility as lr_util
from pattern.SimulationStrategy.Context import SimulationContext


def linear_regression_data_entry_data(data):
    ret_data = dict()

    try:
        alpha = float(data['alpha'])
    except ValueError:
        ret_data['data'] = data['entry'].replace('\"', '').replace('\\r\\n', '\n')
        ret_data['msg'] = 'Wrong format for Alpha'
        return 0, ret_data

    try:
        iterations = int(data['iterations'])
    except ValueError:
        ret_data['data'] = data['entry'].replace('\"', '').replace('\\r\\n', '\n')
        ret_data['msg'] = 'Wrong format for Iterations'
        return 0, ret_data

    try:
        steps = int(data['steps'])
    except ValueError:
        ret_data['data'] = data['entry'].replace('\"', '').replace('\\r\\n', '\n')
        ret_data['msg'] = 'Wrong format for Steps'
        return 0, ret_data

    try:
        theta0 = float(data['theta0'])
        theta1 = float(data['theta1'])
        theta = np.array([theta0, theta1]);
    except ValueError:
        ret_data['data'] = data['entry'].replace('\"', '').replace('\\r\\n', '\n')
        ret_data['msg'] = 'Wrong format for Theta'
        return 0, ret_data

    if steps > iterations:
        ret_data['data'] = data['entry'].replace('\"', '').replace('\\r\\n', '\n')
        ret_data['msg'] = 'Steps should be less than iterations'
        return 0, ret_data

    if iterations % steps != 0:
        iterations -= iterations % steps

    if iterations / steps > 30:
        ret_data['data'] = data['entry'].replace('\"', '').replace('\\r\\n', '\n')
        ret_data['msg'] = 'Either decrease iterations or increase steps.'
        return 0, ret_data

    data = str(json.dumps(data['entry'])).replace("\"", "")
    if lr_util.validate_entry(data) is False:
        ret_data['data'] = data.replace('\"', '').replace('\\r\\n', '\n')
        ret_data['msg'] = 'Wrong Data Format'
        return 0, ret_data

    ret_data['data'] = data.replace('\"', '').replace('\\r\\n', '\n')
    ret_data['msg'] = 'Overshoot occurred. Try lower value of Alpha.'
    data = lr_util.get_matrix(data)

    x = data[0]
    y = data[1]
    x = np.asarray(x)
    y = np.asarray(y)

    simulation_strategy = lr.LinearRegression(theta, x, y, alpha, iterations, steps)
    simulation_context = SimulationContext(simulation_strategy)

    data = simulation_context.get_data()

    if data['overshoot']:
        return 0, ret_data
    posts = db.linear_regression
    post_id = posts.insert_one(data).inserted_id
    return 1, post_id


def linear_regression_simulation(name):
    data = db.linear_regression.find_one({"_id": ObjectId(name)})
    data.pop('_id')
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "ml",
                                            "algo": "lr"})
        if key is not None:
            saved = 1

    return saved, data
