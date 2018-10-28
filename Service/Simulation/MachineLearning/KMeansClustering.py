from flask import render_template, request, redirect, session, Blueprint
from Database.database import db
from classes.Simulation.MachineLearning.KMeansClustering import KMeansClustering as km
from classes.Simulation.MachineLearning.KMeansClustering import Utility as km_util
import random
from bson import ObjectId
from pattern.SimulationStrategy.Context import SimulationContext


def k_means_clustering_simulation(name):
    data = db.k_means_clustering.find_one({"_id": ObjectId(name)})
    data = data['data']
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "ml",
                                            "algo": "km"})
        if key is not None:
            saved = 1
    return saved, data


def k_means_clustering_entry_data(data):
    points = km_util.get_points(data['entry'])
    max_p = 0.0
    min_p = 0.0
    for point in points:
        for entry in point:
            if max_p < entry:
                max_p = entry
            if min_p > entry:
                min_p = entry
    centroids = [[random.uniform(min_p, max_p), random.uniform(min_p, max_p)] for i in range(int(data['clusters']))]

    simulation_strategy = km.KMeans(points, centroids)
    simulation_context = SimulationContext(simulation_strategy)
    data = dict()
    data['data'] = simulation_context.get_data()

    posts = db.k_means_clustering
    post_id = posts.insert_one(data).inserted_id
    return post_id
