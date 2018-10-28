import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, app, Blueprint
from Database.database import db
import classes.Simulation.IterativeDp.Knapsack as knpsck


app = Blueprint('iterative_dp_simulation', __name__)

@app.route("/idp")
def home():
    return render_template(
        '/simulation/iterative_dp_index.html', **locals())