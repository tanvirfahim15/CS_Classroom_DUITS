from bson import ObjectId
from flask import session
from Database.database import db
from pattern.SendNotifications import NotificationSender
from classes.OnlineClassroom.createPost import post


def show_news_feed(course_id):
    pymongo_cursor = db.classroom_newsfeed.find({'course_id':course_id})
    all_data = list(pymongo_cursor)
    data = all_data
    print(data)
    data.reverse()
    print(data)
    course = db.courses.find_one({'_id':ObjectId(course_id)})
    users = course['enrolled']
    if session['username'] not in users:
        NotificationSender.Sender(course_id, "").register_observer(session['username'])
    notifications = db.notifications.find_one({'username': session['username']})
    if notifications == None:
        notifications = []
    else:
        notifications = notifications['notifications']
    notifications.reverse()
    return course, data, users, notifications


def update_post(data , course_id):

    postdetails=post(data['message'],data['files'],session['username'], course_id)
    post_id=save_to_database(postdetails)
    #print(session['username'])
    course = db.courses.find_one({'_id': ObjectId(course_id)})
    course_name = course['course_name']
    notification = {"course_id":course_id, "course_name":course_name, "username": session['username']}
    NotificationSender.Sender(course_id, notification).notify_observer()
    return


def comment_entry(id, course_id):
    course_info = db.courses.find_one({'_id': ObjectId(course_id)})
    notifications = db.notifications.find_one({'username': session['username']})
    if notifications == None:
        notifications = []
    else:
        notifications = notifications['notifications']
    poststring=db.classroom_newsfeed.find_one({'_id': ObjectId(id)});
    pymongo_cursor = db.comments.find( { "postid" : id} )
    all_comments = list(pymongo_cursor)
    comments= all_comments
    notifications.reverse()
    return poststring, comments, course_info, notifications


def update_comment(id , data):
    data = {"posttext": data['message'],"postid":id ,  "authors": session['username']}
    posts = db.comments
    post_id = posts.insert_one(data).inserted_id
    return


def save_to_database(postdetails):
    data = {"posttext": postdetails.getposttext(), "postfile": postdetails.getpostfile(),
            "authors": postdetails.getauthor(), "course_id": postdetails.get_course_id()}
    posts = db.classroom_newsfeed
    return posts.insert_one(data).inserted_id

