from bson import ObjectId
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, session, app, Blueprint
import classes.Calculator.statistics as stat
from Database.database import db

app = Blueprint('statis_calc', __name__)

@app.route("/statistics")
def home():
    return render_template(
        '/calculator/statistical/index.html', **locals())

