from flask import render_template, request, redirect, session, Blueprint
from Service import Profile as service

app = Blueprint('profile', __name__)


@app.route("/profile/<string:username>")
def profile(username):
    if 'username' not in session.keys():
        return redirect('/auth/login')
    if username != session['username']:
        return redirect('/')
    else:
        user_data, data = service.profile()
        return render_template(
            'auth/profile.html', **locals())


@app.route("/profile/save_simulation", methods=['POST', 'GET'])
def save_simulation():
    if request.method == 'POST':
        return service.save_simulation(request.form.to_dict())


@app.route("/profile/remove_simulation", methods=['POST', 'GET'])
def remove_simulation():
    if request.method == 'POST':
        return service.remove_simulation(request.form.to_dict())


# profile end
