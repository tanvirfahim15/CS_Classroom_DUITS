from bson import ObjectId
from flask import render_template, request, redirect, session, app, Blueprint
from Database.database import db
from pattern.SimulationStrategy.Context import SimulationContext

import classes.Simulation.IterativeDp.Fibonacci as dpfib

app = Blueprint('dpfib', __name__)

@app.route("/idp/fib")
def fib():
    simulation_strategy = dpfib.Fibonacci(30)
    simulation_context = SimulationContext(simulation_strategy)
    data = simulation_context.get_data()
    return render_template(
        '/simulation/fibonacci_iterative_dp/fibonacci.html', **locals()
    )