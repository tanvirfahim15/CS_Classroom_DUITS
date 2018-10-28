from flask import render_template, Blueprint

app = Blueprint('dbms_simulation', __name__)


@app.route('/simulation/dbms/')
def dbms():
    return render_template(
        '/simulation/dbms/index.html', **locals()
    )


@app.route('/simulation/dbms/static-hashing')
def static_hashing_simulation():
    return render_template(
        'simulation/dbms/static_hashing/static_hashing.html', **locals())

# dbms/static-hashing end


# dbms/dynamic-hashing start
@app.route('/simulation/dbms/dynamic-hashing')
def dynamic_hashing_simulation():
    return render_template(
        'simulation/dbms/dynamic_hashing/dynamic_hashing.html', **locals())