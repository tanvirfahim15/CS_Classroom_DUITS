import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from pattern.SimulationStrategy.Context import SimulationContext
from Service.Simulation.IterativeDp import CoinChangeVariant3 as ccv3
app = Blueprint('coin_change_variant3', __name__)


@app.route("/idp/coin-change-variant-3/entry", methods=['POST', 'GET'])
def coin_change_variant3_entry():
    return render_template(
        'simulation/coin_change_variant/coin_change_iterative_dp_variant3_entry.html', **locals())


@app.route("/idp/coin-change-variant-3/entry_data", methods=['POST', 'GET'])
def coin_change_variant3_entry_data():
    if request.method == 'POST':
        data = request.form
        post_id = ccv3.coin_change_variant3_entry_data(data)
        return redirect('/idp/coin-change-variant-3/' + str(post_id))
    return redirect('/idp/coin-change-variant-3/entry')


@app.route('/idp/coin-change-variant-3/<string:name>/')
def coin_change_variant3_simulation(name):
    data , saved = ccv3.coin_change_variant3_simulation(name)
    return render_template(
        'simulation/coin_change_variant/coin_change_iterative_dp_variant3_simulation.html', **locals())
