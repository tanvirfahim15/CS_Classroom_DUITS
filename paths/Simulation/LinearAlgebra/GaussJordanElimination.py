from flask import render_template, request, redirect, session, app, Blueprint
from Service.Simulation.LinearAlgebra import GaussJordanElimination as service

app = Blueprint('gauss_jordan_elimination', __name__)


@app.route('/simulation/la/gauss-jordan-elimination/')
def gauss_jordan_elimination():
    name, data, saved = service.gauss_jordan_elimination()
    return render_template(
        'simulation/linear_algebra/gauss_jordan_elimination/gauss_jordan_elimination_simulation.html', **locals())


@app.route('/simulation/la/gauss-jordan-elimination/<string:name>/')
def gauss_jordan_elimination_simulation(name):
    data, saved = service.gauss_jordan_elimination_simulation(name)
    return render_template(
        'simulation/linear_algebra/gauss_jordan_elimination/gauss_jordan_elimination_simulation.html', **locals())


@app.route('/simulation/la/gauss-jordan-elimination/<string:name>/data')
def gauss_jordan_elimination_data(name):
    return service.gauss_jordan_elimination_data(name)


@app.route('/simulation/la/gauss-jordan-elimination/entry')
def gauss_jordan_elimination_entry(data=None):
    return render_template(
        'simulation/linear_algebra/gauss_jordan_elimination/gauss_jordan_elimination_entry.html', **locals())


@app.route('/simulation/la/gauss-jordan-elimination/entry_data', methods=['POST', 'GET'])
def gauss_jordan_elimination_entry_data():
    if request.method == 'POST':
        data = service.gauss_jordan_elimination_entry_data(request.form)
        if data[0] is False:
            return gauss_jordan_elimination_entry(data[1])
        else:
            return redirect('/simulation/la/gauss-jordan-elimination/' + data[1])
    return redirect('/simulation/la/gauss-jordan-elimination/entry')
