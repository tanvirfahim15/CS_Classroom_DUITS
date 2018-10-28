from flask import render_template, request, redirect, session, Blueprint
from Service import Auth as service

app = Blueprint('auth', __name__)


@app.route("/auth/login/")
def login(data=None):
    if 'username' in session.keys():
        return redirect('/profile/'+session['username'])
    return render_template(
        'auth/login.html', **locals())


@app.route("/auth/logout")
def logout():
    if 'username' in session.keys():
        session.pop('username')
    return redirect('/')


@app.route("/auth/login-validation", methods=['POST', 'GET'])
def login_validation():
    if request.method == 'POST':
        flag, data, username = service.login_validation(request.form.to_dict())
        if flag is False:
            return login(data)
        session['username'] = username
        return redirect('/profile/'+session['username'])


@app.route("/auth/register")
def register(data=None):
    if 'username' in session.keys():
        return redirect('/')
    return render_template(
        'auth/register.html', **locals())


@app.route("/auth/change-info")
def change_info(data=None):
    if 'username' not in session.keys():
        return redirect('/')
    if data is None:
        data = service.change_info(data)
    return render_template(
        'auth/change_info.html', **locals())


@app.route("/auth/change-info-validation", methods=['POST', 'GET'])
def change_info_validation():
    if request.method == 'POST':
        flag, data = service.change_info_validation(request.form.to_dict())
        if flag is True:
            return redirect('/profile/'+session['username'])
        return change_info(data)


@app.route("/auth/register-validation", methods=['POST', 'GET'])
def register_validation():
    if request.method == 'POST':
        flag, data = service.register_validation(request.form.to_dict())
        if flag:
            return redirect('/auth/login')
        return register(data)

