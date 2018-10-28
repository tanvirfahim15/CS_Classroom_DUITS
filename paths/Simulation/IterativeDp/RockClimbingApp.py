import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from Service.Simulation.IterativeDp import RockClimbing as rc
from pattern.SimulationStrategy.Context import SimulationContext

app = Blueprint('rock_climbing', __name__)


@app.route("/idp/rock-climbing/entry", methods=['POST', 'GET'])
def rock_climbing_entry():
    return render_template(
        'simulation/rockclimbing_iterative_dp/rockclimbing_iterative_dp_entry.html', **locals())


@app.route("/idp/rock-climbing/entry_data", methods=['POST', 'GET'])
def rock_climbing_entry_data():
    if request.method == 'POST':
        data = request.form
        post_id = rc.rock_climbing_entry_data(data)
        return redirect('/idp/rock-climbing/' + str(post_id))
    return redirect('/idp/rock-climbing/entry')


@app.route('/idp/rock-climbing/<string:name>/')
def rock_climbing_simulation(name):
    data , saved = rc.rock_climbing_simulation(name)
    return render_template(
        'simulation/rockclimbing_iterative_dp/rockclimbing_iterative_dp_simulation.html', **locals())