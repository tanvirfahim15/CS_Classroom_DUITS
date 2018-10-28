from flask import render_template, request, redirect, session, app, Blueprint
from Service.Simulation.LinearAlgebra import GaussElimination as service

app = Blueprint('gauss_elimination', __name__)


@app.route('/simulation/la/gauss-elimination/')
def gauss_elimination():
    data, saved, name = service.gauss_elimination()
    return render_template(
        'simulation/linear_algebra/gauss_elimination/gauss_elimination_simulation.html', **locals())


@app.route('/simulation/la/gauss-elimination/<string:name>/')
def gauss_elimination_simulation(name):
    data, saved = service.gauss_elimination_simulation(name)
    return render_template(
        'simulation/linear_algebra/gauss_elimination/gauss_elimination_simulation.html', **locals())


@app.route('/simulation/la/gauss-elimination/<string:name>/data')
def gauss_elimination_data(name):
    return service.gauss_elimination_data(name)


@app.route('/simulation/la/gauss-elimination/entry')
def gauss_elimination_entry(data=None):
    return render_template(
        'simulation/linear_algebra/gauss_elimination/gauss_elimination_entry.html', **locals())


@app.route('/simulation/la/gauss-elimination/entry_data', methods=['POST', 'GET'])
def gauss_elimination_entry_data():
    if request.method == 'POST':
        data = service.gauss_elimination_entry_data(request.form)
        if data[0] is False:
            return gauss_elimination_entry(data[1])
        else:
            return redirect('/simulation/la/gauss-elimination/' + data[1])
    return redirect('/simulation/la/gauss-elimination/entry')
