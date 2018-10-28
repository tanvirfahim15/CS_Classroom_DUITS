from flask import render_template, request, redirect, session, Blueprint
from utility import Country
from Database.database import db


def profile():
    user_data = db.users.find_one({'username': session['username']})
    user_data['country'] = Country.country[user_data['country']]
    posts = db.saved_simulation.find({'username': session['username']})
    data = []
    for post in posts:
        post.pop('_id')
        data.append(post)
    return user_data, data


def save_simulation(data):
    posts = db.saved_simulation
    posts.insert_one(data)
    return str('saved')


def remove_simulation(data):
    posts = db.saved_simulation
    posts.remove(data)
    return str('removed')
