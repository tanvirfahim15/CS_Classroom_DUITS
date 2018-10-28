from flask import render_template, request, session, Blueprint, redirect
from Service.Blog import Read as service
from classes.Blog.Qpredict import Qpredict
from pattern.SearchArticle import SearchStrategy

app = Blueprint('blog_read', __name__)


@app.route('/blog/profile/<string:id>/')
def blog_profile(id):
    user, articles, subscribed, own = service.blog_profile(id)
    return render_template('/blog/profile.html', **locals())


@app.route('/blog/newsfeed/')
def blog_newsfeed():
    if 'username' not in session.keys():
        return redirect('/auth/login/')
    articles = service.blog_newsfeed()
    return render_template('/blog/newsfeed.html', **locals())


@app.route('/blog/qpredict/<string:id>/')
def blog_qpredict(id):
    questions = Qpredict.Qpredict(service.blog_qpredict(id))
    return render_template('/blog/qpredict.html', **locals())


@app.route('/blog/search/', methods=['GET', 'POST'])
def blog_search():
    if request.method == 'POST':
        data, articles = service.blog_search(True, request.form)
    else:
        data, articles = service.blog_search(False, None)
    return render_template('/blog/search.html', **locals())

