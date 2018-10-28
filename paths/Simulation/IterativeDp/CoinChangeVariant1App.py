import ast
from bson import ObjectId
from flask import render_template, request, redirect, session,  Blueprint
from Service.Simulation.IterativeDp import CoinChangeVariant1 as ccv1
from pattern.SimulationStrategy.Context import SimulationContext


app = Blueprint('coin_change_variant1', __name__)


@app.route("/idp/coin-change")
def coin_change():
    return render_template(
        'simulation/coin_change_variant/coin_change.html', **locals())


# idp/coin change variant-1 start
@app.route("/idp/coin-change-variant-1/entry", methods=['POST', 'GET'])
def coin_change_variant1_entry():
    return render_template(
        'simulation/coin_change_variant/coin_change_iterative_dp_variant1_entry.html', **locals())


@app.route("/idp/coin-change-variant-1/entry_data", methods=['POST', 'GET'])
def coin_change_variant1_entry_data():
    if request.method == 'POST':
        data = request.form
        post_id = ccv1.coin_change_variant1_entry_data(data)
        return redirect('/idp/coin-change-variant-1/' + str(post_id))
    return redirect('/idp/coin-change-variant-1/entry')


@app.route('/idp/coin-change-variant-1/<string:name>/')
def coin_change_variant1_simulation(name):
    data , saved = ccv1.coin_change_variant1_simulation(name)
    return render_template(
        'simulation/coin_change_variant/coin_change_iterative_dp_variant1_simulation.html', **locals())