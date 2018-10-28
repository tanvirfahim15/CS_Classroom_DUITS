from flask import render_template, Blueprint

app = Blueprint('machine_learning_simulation', __name__)


@app.route('/simulation/ml/')
def machine_learning():
    return render_template(
        '/simulation/machine_learning/index.html', **locals()
    )
