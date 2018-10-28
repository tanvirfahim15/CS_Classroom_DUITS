from flask import render_template, request, redirect, session, Blueprint
from Database.database import db
from classes.Simulation.MachineLearning.LogisticRegression import LogisticRegression as lgr
from classes.Simulation.MachineLearning.LogisticRegression import Utility as lgr_util
import numpy as np
from bson import ObjectId
from pattern.SimulationStrategy.Context import SimulationContext


def logistic_regression_simulation(name):
    data = db.logistic_regression.find_one({"_id": ObjectId(name)})
    data.pop('_id')
    max_iter = len(data['data']) / 5
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "ml",
                                            "algo": "lgr"})
        if key is not None:
            saved = 1
    return saved, max_iter, data


def logistic_regression_data_entry_data(data):
    iterations = int(data['iterations'])
    steps = int(data['steps'])
    alpha = float(data['alpha'])
    data = lgr_util.get_data(data['entry'])
    x1 = data[0]
    x2 = data[1]
    y = np.asarray(data[2])
    x = lgr_util.combine(x1, x2)
    simulation_strategy = lgr.LogisticRegression(x, y, iterations, steps, alpha)
    simulation_context = SimulationContext(simulation_strategy)

    data = dict()
    data['data'] = simulation_context.get_data()
    data['x1'] = x1
    data['x2'] = x2
    data['y'] = list(y)
    data['alpha'] = alpha
    posts = db.logistic_regression
    post_id = posts.insert_one(data).inserted_id
    return post_id
