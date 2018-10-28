from flask import render_template, request, redirect, Blueprint
from Service.Simulation.MachineLearning import LinearRegression as service

app = Blueprint('linear_regression', __name__)


@app.route('/simulation/ml/linear-regression/')
def linear_regression():
    return redirect('/simulation/ml/linear-regression/5b883b3b76cc9d150046f9ab')


@app.route("/simulation/ml/linear-regression/entry")
def linear_regression_data_entry(data=None):
    return render_template(
        'simulation/machine_learning/linear_regression/linear_regression_entry.html', **locals())


@app.route("/simulation/ml/linear-regression/entry_data", methods=['POST', 'GET'])
def linear_regression_data_entry_data():
    if request.method == 'POST':
        data = service.linear_regression_data_entry_data(request.form)
        if data[0] == 0:
            return linear_regression_data_entry(data[1])
        return redirect('/simulation/ml/linear-regression/' + str(data[1]))


@app.route('/simulation/ml/linear-regression/<string:name>')
def linear_regression_simulation(name):
    saved, data = service.linear_regression_simulation(name)
    return render_template(
        'simulation/machine_learning/linear_regression/linear_regression_simulation.html', **locals())

