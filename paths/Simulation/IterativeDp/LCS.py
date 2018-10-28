from flask import render_template, request, redirect, session, app, Blueprint
from Service.Simulation.IterativeDp import LCS as service

app = Blueprint('lcs-idp', __name__)


# idp/longest common subsequence start
@app.route("/simulation/idp/longest-common-subsequence/")
def longest_common_subsequence():
    data, saved = service.longest_common_subsequence()
    return render_template(
        'simulation/iterative_dp/lcs_iterative_dp/lcs_iterative_dp_simulation.html', **locals())


@app.route("/simulation/idp/longest-common-subsequence/entry", methods=['POST', 'GET'])
def longest_common_subsequence_entry():
    return render_template(
        'simulation/iterative_dp/lcs_iterative_dp/lcs_iterative_dp_entry.html', **locals())


@app.route("/simulation/idp/longest-common-subsequence/entry_data", methods=['POST', 'GET'])
def longest_common_subsequence_entry_data():
    if request.method == 'POST':
        post_id = service.longest_common_subsequence_entry_data(request.form)
        return redirect('/simulation/idp/longest-common-subsequence/' + str(post_id))
    return redirect('/simulation/idp/longest-common-subsequence/entry')


@app.route('/simulation/idp/longest-common-subsequence/<string:name>/')
def longest_common_subsequence_simulation(name):
    data, saved = service.longest_common_subsequence_simulation(name)
    return render_template(
        'simulation/iterative_dp/lcs_iterative_dp/lcs_iterative_dp_simulation.html', **locals())
