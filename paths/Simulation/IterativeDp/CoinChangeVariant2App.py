import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from pattern.SimulationStrategy.Context import SimulationContext
from Service.Simulation.IterativeDp import CoinChangeVariant2 as ccv2

app = Blueprint('coin_change_variant2', __name__)


@app.route("/idp/coin-change-variant-2/entry", methods=['POST', 'GET'])
def coin_change_variant2_entry():
    return render_template(
        'simulation/coin_change_variant/coin_change_iterative_dp_variant2_entry.html', **locals())


@app.route("/idp/coin-change-variant-2/entry_data", methods=['POST', 'GET'])
def coin_change_variant2_entry_data():
    if request.method == 'POST':
        data = request.form
        post_id = ccv2.coin_change_variant2_entry_data(data)
        return redirect('/idp/coin-change-variant-2/' + str(post_id))
    return redirect('/idp/coin-change-variant-2/entry')


@app.route('/idp/coin-change-variant-2/<string:name>/')
def coin_change_variant2_simulation(name):
    data , saved = ccv2.coin_change_variant2_simulation(name)
    return render_template(
        'simulation/coin_change_variant/coin_change_iterative_dp_variant2_simulation.html', **locals())

