from flask import request, session, Blueprint
import classes.Blog.Subscription.Writer as Writer_Subject

app = Blueprint('blog_subscribe', __name__)


@app.route('/blog/subscribe/<string:writer>', methods=['POST', 'GET'])
def blog_subscribe(writer):
    if request.method == 'POST':
        if 'username' in session.keys():
            Writer_Subject.Writer(writer).register_observer(session['username'])
            return 'Subscribed'


@app.route('/blog/unsubscribe/<string:writer>', methods=['POST', 'GET'])
def blog_unsubscribe(writer):
    if request.method == 'POST':
        if 'username' in session.keys():
            Writer_Subject.Writer(writer).remove_observer(session['username'])
            return 'Unsubscribed'
