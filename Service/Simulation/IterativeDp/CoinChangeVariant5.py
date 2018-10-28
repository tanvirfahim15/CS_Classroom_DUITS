import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from Database.database import db
from classes.Simulation.IterativeDp import CoinChangeVariant5 as ccv5
from pattern.SimulationStrategy.Context import SimulationContext


def coin_change_variant5_entry_data(data):
    data = {'coin_array_variant5': data['coin_array_variant5'],'payment_variant5': data['payment_variant5']}
    posts = db.coin_change_variant5
    post_id = posts.insert_one(data).inserted_id
    return post_id


def coin_change_variant5_simulation(name):
    data = db.coin_change_variant5.find_one({"_id": ObjectId(name)})
    coin_array1 = ast.literal_eval(data['coin_array_variant5'])
    coin_array2 = []
    coin_array2.append(0)
    for i in range(len(coin_array1)):
        coin_array2.append(int(coin_array1[i]))
    k = len(coin_array1)
    payment = data['payment_variant5']

    dp_simulation_strategy = ccv5.CoinChangeVariant5(int(payment), k , coin_array2)
    dp_simulation_context = SimulationContext(dp_simulation_strategy)
    data = dp_simulation_context.get_data()

    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "coin_change_variant5"})
        if key is not None:
            saved = 1
    return data, saved
