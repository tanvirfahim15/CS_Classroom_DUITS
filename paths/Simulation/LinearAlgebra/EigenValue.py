from flask import render_template, request, redirect, session, app, Blueprint
from Service.Simulation.LinearAlgebra import EigenValue as service

app = Blueprint('eigen-value', __name__)


@app.route('/simulation/la/eigen-value/', methods=['POST', 'GET'])
def eigen_value():
    name, data, saved = service.eigen_value()
    return render_template(
        'simulation/linear_algebra/eigen_value/eigen_value_simulaion.html', **locals())


@app.route('/simulation/la/eigen-value/<string:name>/', methods=['POST', 'GET'])
def eigen_value_simulation(name):
    data, saved = service.eigen_value_simulation(name)
    return render_template(
        'simulation/linear_algebra/eigen_value/eigen_value_simulaion.html', **locals())


@app.route('/simulation/la/eigen-value/entry_data', methods=['POST', 'GET'])
def eigen_value_entry_data():
    if request.method == 'POST':
        data = service.eigen_value_entry_data(request.form)
        if data[0] is False:
            return eigen_value_entry(data[1])
        else:
            return redirect("/simulation/la/eigen-value/"+data[1])


@app.route('/simulation/la/eigen-value/entry')
def eigen_value_entry(data=None):
    return render_template(
        'simulation/linear_algebra/eigen_value/eigen_value_entry.html', **locals())
