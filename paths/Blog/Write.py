from bson import ObjectId
from flask import render_template, flash, redirect, request, session, Blueprint, url_for
from wtforms import Form, StringField, TextAreaField, validators
import classes.Blog.Subscription.Writer as Writer
from Database.database import db
import datetime
from paths.Blog.BlogArticleConcreteStrategy import BlogArticleConcreteStrategy, Context
from Service.Blog import Read as read

app = Blueprint('blog_write', __name__)

now = datetime.datetime.now()



@app.route('/articles')
def articles():
    articles = read.blog_article_find(None, None)

    if articles is not None:
        return render_template('/tutorial/articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('/tutorial/articles.html', msg=msg)


@app.route('/article/<string:id>/')
def article(id):
    #articles = db.article.find({"_id": ObjectId(id)})
    articles = read.blog_article_find(id, None)
    print(articles)
    return render_template('/tutorial/article.html', articles=articles,id=id)


@app.route('/dashboard')
def dashboard():
    #articles = db.article.find({"author": session['username']})
    articles = read.blog_article_find(None, session['username'])

    if articles is not None:
        return render_template('/tutorial/dashboard.html', articles=articles)
    else:
        msg = 'You Do Not Have Any Articles'
        return render_template('/tutorial/dashboard.html', msg=msg)


class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=4)])


@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        concrete_strategy = BlogArticleConcreteStrategy()
        articles = Context(concrete_strategy)
        articles.context_interface()
        articles.setTitle(form.title.data)
        articles.setBody(form.body.data)
        articles.setAuthor(session['username'])

        # title = form.title.data
        # body = form.body.data
        # author = session['username']

        #article_id = db.article.insert({"title": articles.getTitle(), "author": articles.getAuthor(), "body": articles.getBody(), "date": str(now)})
        article_id = read.blog_artcile_insert(articles)
        article_id = str(article_id)
        flash('Article Created', 'success')
        Writer.Writer(session['username']).notify_observer(article_id)
        return redirect('/article/'+article_id+'/')

    return render_template('/tutorial/add_article.html', form=form)


@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
def edit_article(id):
    articles = db.article.find_one({"_id": ObjectId(id)})
    #articles = read.blog_article_find(id, None)
    form = ArticleForm(request.form)

    form.title.data = articles['title']
    form.body.data = articles['body']



    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        articles['title'] = title
        articles['body'] = body
        read.blog_article_save(articles)

        flash('Article Updated', 'success')
        return redirect(url_for('blog_write.dashboard'))
    return render_template('/tutorial/edit_article.html', form=form)

@app.route('/delete_article/<string:id>', methods=['GET', 'POST'])
def delete_article(id):
    #db.article.remove({"_id": ObjectId(id)})
    read.blog_article_remove(id)
    flash('Article Deleted', 'success')
    return redirect(url_for('blog_write.dashboard'))

@app.route('/online_forum/forum_home')
def forum_home():
    return render_template('/tutorial/forum_home.html', **locals())



