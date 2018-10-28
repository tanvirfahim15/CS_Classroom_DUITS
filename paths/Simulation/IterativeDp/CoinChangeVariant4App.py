import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from Service.Simulation.IterativeDp import CoinChangeVariant4 as ccv4
from pattern.SimulationStrategy.Context import SimulationContext
app = Blueprint('coin_change_variant4', __name__)


@app.route("/idp/coin-change-variant-4", methods=['POST', 'GET'])
def coin_change_variant4_entry():
    return render_template(
        'simulation/coin_change_variant/coin_change_iterative_dp_variant4_entry.html', **locals())


@app.route("/idp/coin-change-variant-4/entry_data", methods=['POST', 'GET'])
def coin_change_variant4_entry_data():
    if request.method == 'POST':
        data = request.form
        post_id = ccv4.coin_change_variant4_entry_data(data)
        return redirect('/idp/coin-change-variant-4/' + str(post_id))
    return redirect('/idp/coin-change-variant-4/entry')


@app.route('/idp/coin-change-variant-4/<string:name>/')
def coin_change_variant4_simulation(name):
    data, saved = ccv4.coin_change_variant4_simulation(name)
    return render_template(
        'simulation/coin_change_variant/coin_change_iterative_dp_variant4_simulation.html', **locals())
