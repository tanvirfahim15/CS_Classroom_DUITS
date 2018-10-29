from flask import Blueprint
from flask import render_template, request, redirect, session,jsonify
from Service.OnlineClassroom import ClassroomFeed as service

from pattern.AdapterPattern.addclasstopost import addclasstopost
from pattern.AdapterPattern.assignmenttopost import assignmenttopost

app = Blueprint('classroom_feed', __name__)


@app.route("/news-feed/<course_id>")
def show_news_feed(course_id):
    #course_id ='5bd316f051b1980fab57b706'
    course_info, data, users, notifications = service.show_news_feed(course_id)
    classmate_count = len(course_info['enrolled'])
    return render_template('OnlineClassroom/post_and_comment/feed.html', **locals())


@app.route("/entry_data/<course_id>" , methods=['POST', 'GET'])
def update_post(course_id):
    #course_id = '5bd316f051b1980fab57b706'
    if request.method=="POST":
        data = request.form
        service.update_post(data , course_id)
    return redirect('/news-feed/'+str(course_id))


@app.route("/comment_entry/<id>/<course_id>" , methods=['POST', 'GET'])
def comment_entry(id, course_id):
    poststring , comments , course_info , notifications= service.comment_entry(id, course_id)
    classmate_count = len(course_info['enrolled'])
    return render_template('OnlineClassroom/post_and_comment/comment.html' ,**locals())


@app.route("/entry_comment/<id>/<course_id>" , methods=['POST', 'GET'])
def update_comment(id, course_id):
    if request.method=="POST":
        data = request.form
        service.update_comment(id ,data)
    return redirect('/comment_entry/'+str(id)+'/'+str(course_id))


@app.route("/assignment/<course_id>")
def assingmnet(course_id):
    return render_template('OnlineClassroom/post_and_comment/giveassignment.html', **locals())


@app.route('/add_assignment/<course_id>')
def add_assignment(course_id):
    time = request.args.get('time', 0, type=str)
    date = request.args.get('date', 0, type=str)
    details= request.args.get('details', 0, type=str)
    print(time)
    print(date)
    print(details)
    assignmenttopost(time,date,details,session['username'],course_id)
    return jsonify(result="assignment added")


@app.route('/class/<course_id>')
def class_add(course_id):
    return render_template('OnlineClassroom/post_and_comment/addclass.html', **locals() )


@app.route('/add_class/<course_id>')
def add_class(course_id):
    starttime = request.args.get('starttime', 0, type=str)
    endtime = request.args.get('endtime', 0, type=str)
    details= request.args.get('details', 0, type=str)
    print(starttime)
    print(endtime)
    print(details)
    addclasstopost(starttime,endtime,details,session['username'],course_id)
    return jsonify(result="new class time has been announced")