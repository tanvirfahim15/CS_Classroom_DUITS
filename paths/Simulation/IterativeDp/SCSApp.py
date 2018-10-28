import  ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from Service.Simulation.IterativeDp import SCS as scs
from pattern.SimulationStrategy.Context import SimulationContext

app = Blueprint('scs', __name__)


@app.route("/idp/shortest-common-supersequence/entry", methods=['POST', 'GET'])
def shortest_common_supersequence_entry():
    return render_template(
        'simulation/scs_iterative_dp/scs_iterative_dp_entry.html', **locals())


@app.route("/idp/shortest-common-supersequence/entry_data", methods=['POST', 'GET'])
def shortest_common_supersequence_entry_data():
    if request.method == 'POST':
        data = request.form
        post_id = scs.shortest_common_supersequence_entry_data(data)
        return redirect('/idp/shortest-common-supersequence/' + str(post_id))
    return redirect('/idp/shortest-common-supersequence/entry')


@app.route('/idp/shortest-common-supersequence/<string:name>/')
def shortest_common_supersequence_simulation(name):
    data, saved = scs.shortest_common_supersequence_simulation(name)
    return render_template(
        'simulation/scs_iterative_dp/scs_iterative_dp_simulation.html', **locals())