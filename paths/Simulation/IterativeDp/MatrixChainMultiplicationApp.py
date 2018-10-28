import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from pattern.SimulationStrategy.Context import SimulationContext
from Service.Simulation.IterativeDp import MatrixChainMultiplication as mcm
app = Blueprint('matrix_chain_multiplication', __name__)


@app.route("/idp/matrix-chain-multiplication/entry", methods=['POST', 'GET'])
def matrix_chain_multiplication_entry():
    return render_template(
        'simulation/mcm_iterative_dp/mcm_iterative_dp_entry.html', **locals())


@app.route("/idp/matrix-chain-multiplication/entry_data", methods=['POST', 'GET'])
def matrix_chain_multiplication_data_entry():
    if request.method == 'POST':
        data = request.form
        post_id = mcm.matrix_chain_multiplication_data_entry(data)
        return redirect('/idp/matrix-chain-multiplication/' + str(post_id))
    return redirect('/idp/matrix-chain-multiplication/entry')


@app.route('/idp/matrix-chain-multiplication/<string:name>/')
def matrix_chain_multiplication_simulation(name):
    data, saved = mcm.matrix_chain_multiplication_simulation(name)
    return render_template(
        'simulation/mcm_iterative_dp/mcm_iterative_dp_simulation.html', **locals())