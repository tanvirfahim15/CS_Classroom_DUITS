from flask import Blueprint
from flask import render_template, request, redirect, session,jsonify
from Service.OnlineClassroom import ClassroomFeed as service

from pattern.AdapterPattern.addclasstopost import addclasstopost
from pattern.AdapterPattern.assignmenttopost import assignmenttopost

app = Blueprint('classroom_feed', __name__)


@app.route("/news-feed")
def show_news_feed():
    course_id ='5bd316f051b1980fab57b706'
    data, users, notifications = service.show_news_feed(course_id)
    return render_template('OnlineClassroom/post_and_comment/feed.html', **locals())


@app.route("/entry_data" , methods=['POST', 'GET'])
def update_post():
    course_id = '5bd316f051b1980fab57b706'
    if request.method=="POST":
        data = request.form
        service.update_post(data , course_id)
    return redirect('/news-feed')


@app.route("/comment_entry/<id>" , methods=['POST', 'GET'])
def comment_entry(id):
    poststring , comments = service.comment_entry(id)
    return render_template('OnlineClassroom/post_and_comment/comment.html' ,**locals())


@app.route("/entry_comment/<id>" , methods=['POST', 'GET'])
def update_comment(id):
    if request.method=="POST":
        data = request.form
        service.update_comment(id ,data)
    return redirect('/comment_entry/'+str(id))


@app.route("/assignment")
def assingmnet():
    return render_template('OnlineClassroom/post_and_comment/giveassignment.html')


@app.route('/add_assignment')
def add_assignment():
    time = request.args.get('time', 0, type=str)
    date = request.args.get('date', 0, type=str)
    details= request.args.get('details', 0, type=str)
    print(time)
    print(date)
    print(details)
    assignmenttopost(time,date,details,session['username'])
    return jsonify(result="assignment added")


@app.route('/class')
def class_add():
    return render_template('OnlineClassroom/post_and_comment/addclass.html')


@app.route('/add_class')
def add_class():
    starttime = request.args.get('starttime', 0, type=str)
    endtime = request.args.get('endtime', 0, type=str)
    details= request.args.get('details', 0, type=str)
    print(starttime)
    print(endtime)
    print(details)
    addclasstopost(starttime,endtime,details,session['username'])
    return jsonify(result="new class time has been announced")