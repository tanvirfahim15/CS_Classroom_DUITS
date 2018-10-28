from flask import render_template, request, redirect, Blueprint
from classes.Simulation.MachineLearning.KMeansClustering import Utility as km_util
from Service.Simulation.MachineLearning import KMeansClustering as service

app = Blueprint('k_means_clustering', __name__)


@app.route('/simulation/ml/k-means-clustering/')
def k_means_clustering():
    name = '5b8842c376cc9d18036c6eb4'
    return k_means_clustering_simulation(name)


@app.route('/simulation/ml/k-means-clustering/<string:name>')
def k_means_clustering_simulation(name):
    saved, data = service.k_means_clustering_simulation(name)
    return render_template(
        'simulation/machine_learning/k_means_clustering/k_means_clustering_simulation.html', **locals()
    )


@app.route('/simulation/ml/k-means-clustering/entry')
def k_means_clustering_entry(data=None):
    return render_template(
        'simulation/machine_learning/k_means_clustering/k_means_clustering_entry.html', **locals()
    )


@app.route('/simulation/ml/k-means-clustering/entry-data', methods=['POST', 'GET'])
def k_means_clustering_entry_data():
    if request.method == 'POST':
        data = request.form.to_dict()
        if km_util.validate_entry(data['entry']) is False:
            return k_means_clustering_entry(data)
        post_id = service.k_means_clustering_entry_data(data)
        return redirect('simulation/ml/k-means-clustering/' + str(post_id))


