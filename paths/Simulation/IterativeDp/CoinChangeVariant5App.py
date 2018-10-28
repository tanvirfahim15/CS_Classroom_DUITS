import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from Service.Simulation.IterativeDp import CoinChangeVariant5 as ccv5
from pattern.SimulationStrategy.Context import SimulationContext
app = Blueprint('coin_change_variant5', __name__)


@app.route("/idp/coin-change-variant-5/entry", methods=['POST', 'GET'])
def coin_change_variant5_entry():
    return render_template(
        'simulation/coin_change_variant/coin_change_iterative_dp_variant5_entry.html', **locals())


@app.route("/idp/coin-change-variant-5/entry_data", methods=['POST', 'GET'])
def coin_change_variant5_entry_data():
    if request.method == 'POST':
        data = request.form
        post_id = ccv5.coin_change_variant5_entry_data(data)
        return redirect('/idp/coin-change-variant-5/' + str(post_id))
    return redirect('/idp/coin-change-variant-5/entry')


@app.route('/idp/coin-change-variant-5/<string:name>/')
def coin_change_variant5_simulation(name):
    data , saved = ccv5.coin_change_variant5_simulation(name)
    return render_template(
        'simulation/coin_change_variant/coin_change_iterative_dp_variant5_simulation.html', **locals())
