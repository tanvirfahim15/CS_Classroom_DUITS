from flask import render_template, Blueprint

app = Blueprint('gauss_elimination_simulation', __name__)


@app.route('/simulation/la/')
def gauss_elimination():
    return render_template(
        '/simulation/linear_algebra/index.html', **locals()
    )
