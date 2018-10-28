from flask import render_template, request, redirect, Blueprint
from classes.Simulation.MachineLearning.LogisticRegression import Utility as lgr_util
from Service.Simulation.MachineLearning import LogisticRegression as service

app = Blueprint('logistic_regression', __name__)


@app.route('/simulation/ml/logistic-regression/')
def logistic_regression():
    name = '5b88479676cc9d1a09a1aeb5'
    return logistic_regression_simulation(name)


@app.route('/simulation/ml/logistic-regression/<string:name>')
def logistic_regression_simulation(name):
    saved, max_iter, data = service.logistic_regression_simulation(name)
    return render_template(
        '/simulation/machine_learning/logistic_regression/logistic_regression_simulation.html', **locals()
    )


@app.route('/simulation/ml/logistic-regression/entry')
def logistic_regression_data_entry(data=None):
    return render_template(
        '/simulation/machine_learning/logistic_regression/logistic_regression_entry.html', **locals()
    )


@app.route('/simulation/ml/logistic-regression/entry-data', methods=['POST', 'GET'])
def logistic_regression_data_entry_data():
    if request.method == 'POST':
        data = request.form.to_dict()
        if lgr_util.validate_entry(data) is False:
            return logistic_regression_data_entry(data)
        post_id = service.logistic_regression_data_entry_data(data)
        return redirect('/simulation/ml/logistic-regression/' + str(post_id))
