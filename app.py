import flask_login
from flask import Flask, render_template, session, flash
from flask_login import LoginManager

from Database.database import db
from paths.Auth import app as auth
from paths.Profile import app as profile
from paths.Simulation.MachineLearning.main import app as machine_learning_simulation
from paths.Simulation.MachineLearning.LinearRegression import app as linear_regression
from paths.Simulation.MachineLearning.LogisticRegression import app as logistic_regression
from paths.Simulation.MachineLearning.KMeansClustering import app as k_means_clustering
from paths.Blog.Write import app as online_forum
from paths.Blog.Read import app as blog_read
from paths.Blog.Subscription import app as blog_subscription
from paths.CodeGenerator import app as code_generator
import utility.flask_loginmanager as log
from paths.OnlineIde.ide import app as online_ide
from paths.Simulation.IterativeDp.KnapsackApp import app as knpsack
from paths.Simulation.IterativeDp.main import app as iterative_dp_simulation
from paths.Simulation.IterativeDp.EditDistanceApp import app as edit_distance
from paths.Simulation.IterativeDp.LISApp import app as lis
from paths.Simulation.IterativeDp.FibonacciApp import app as dpfib
from paths.Simulation.IterativeDp.LCS import app as lcs
from paths.Simulation.IterativeDp.CoinChangeVariant1App import app as ccv1
from paths.Simulation.IterativeDp.CoinChangeVariant2App import app as ccv2
from paths.Simulation.IterativeDp.CoinChangeVariant3App import app as ccv3
from paths.Simulation.IterativeDp.CoinChangeVariant4App import app as ccv4
from paths.Simulation.IterativeDp.CoinChangeVariant5App import app as ccv5
from paths.Simulation.IterativeDp.MatrixChainMultiplicationApp import app as mcm
from paths.Simulation.IterativeDp.SCSApp import app as scs
from paths.Simulation.IterativeDp.RockClimbingApp import app as rc
from paths.OnlineClassroom.ClassroomFeed import app as classroom_feed
from paths.Simulation.LinearAlgebra.GaussJordanElimination import app as gauss_jordan_elimination
from paths.Simulation.LinearAlgebra.GaussElimination import app as gauss_elimination
from paths.Simulation.LinearAlgebra.EigenValue import app as eigen_value
from paths.Simulation.LinearAlgebra.main import app as linear_algebra
from paths.Simulation.DBMS.main import app as dbms
from paths.StatisticalCalculator.DeviationCalculator import app as dev_calc
from paths.StatisticalCalculator.FrequencyCalculator import app as freq_calc
from paths.StatisticalCalculator.main import app as statis_calc
from paths.StatisticalCalculator.BoxPlot import app as box_plot

app = Flask(__name__)
app.secret_key = 'UIBBN*E(DNJ'


app.register_blueprint(auth)
app.register_blueprint(profile)

# Simulation paths
app.register_blueprint(machine_learning_simulation)
app.register_blueprint(linear_regression)
app.register_blueprint(logistic_regression)
app.register_blueprint(k_means_clustering)

# Online Forum paths
app.register_blueprint(online_forum)
app.register_blueprint(blog_read)
app.register_blueprint(blog_subscription)

log.login_manager.init_app(app)

# Online Editor paths
app.register_blueprint(online_ide)

# Code generator paths
app.register_blueprint(code_generator)

# Iterative Dp paths
app.register_blueprint(iterative_dp_simulation)
app.register_blueprint(knpsack)
app.register_blueprint(edit_distance)
app.register_blueprint(lis)
app.register_blueprint(dpfib)
app.register_blueprint(lcs)
app.register_blueprint(ccv1)
app.register_blueprint(ccv2)
app.register_blueprint(ccv3)
app.register_blueprint(ccv4)
app.register_blueprint(ccv5)
app.register_blueprint(mcm)
app.register_blueprint(scs)
app.register_blueprint(rc)

# Linear Algebra Path
app.register_blueprint(linear_algebra)
app.register_blueprint(gauss_elimination)
app.register_blueprint(gauss_jordan_elimination)
app.register_blueprint(eigen_value)

# DBMS path
app.register_blueprint(dbms)


# Online Classroom
app.register_blueprint(classroom_feed)


# Statistical Calculator
app.register_blueprint(statis_calc)
app.register_blueprint(freq_calc)
app.register_blueprint(dev_calc)
app.register_blueprint(box_plot)


@app.route("/")
def home():
    return render_template(
        'home.html', **locals())


if __name__ == "__main__":
    app.run()
