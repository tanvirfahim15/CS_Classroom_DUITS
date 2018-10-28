import datetime

from Database.database import db
import classes.Blog.Subscription.Writer as Writer_Subject
from flask import session
from bson import ObjectId
from paths.Blog.BlogArticleConcreteStrategy import BlogArticleConcreteStrategy, Context
from pattern.SearchArticle import SearchStrategy

now = datetime.datetime.now()


def blog_profile(id):
    user = db.users.find_one({'username': id})
    articles = db.article.find({"author": id})
    if 'username' in session.keys():
        subscribed = Writer_Subject.Writer(id).find_observer(session['username'])
    else:
        subscribed = False
    own = None
    if session['username'] == id:
        own = True
    return user, articles, subscribed, own


def blog_newsfeed():
    writers = []
    for writer in db.subsription.find():
        if session['username'] in writer['readers']:
            writers.append(writer['writer_id'])
    articles = []
    for writer in writers:
        article_s=db.article.find({'author': writer})
        for article in article_s:
            articles.append(article)
    articles = sorted(articles, key=lambda k: k['date'], reverse=True)
    return articles


def blog_qpredict(id):
    return db.article.find_one({"_id": ObjectId(id)})['body']


def blog_search(post, data):
    if post:
        search_strategy = None
        if data['class'] == 'and':
            search_strategy = SearchStrategy.AndSearchStrategy(data['gender'], data['institute'], data['country'], data['author_name'], data['article_name'])
        else:
            search_strategy = SearchStrategy.OrSearchStrategy(data['gender'], data['institute'], data['country'], data['author_name'], data['article_name'])

        search_context = SearchStrategy.SearchContext(search_strategy)
        articles = search_context.get_articles()
        return data, articles
    else:

        data = dict()
        data['article_name'] = ''
        data['author_name'] = ''
        data['institute'] = ''
        data['gender'] = '0'
        data['country'] = '0'
        data['class'] = 'and'
        articles = []
        return data, articles



def blog_article_find(id, author):
    if id == None and author == None:
        return db.article.find()
    elif author == None:
        return db.article.find({"_id": ObjectId(id)})
    else:
        return db.article.find({"author": session['username']})

def blog_article_save(articles):
    db.article.save(articles)

def blog_article_remove(id):
    db.article.remove({"_id": ObjectId(id)})

def blog_artcile_insert(articles):
    return db.article.insert(
        {"title": articles.getTitle(), "author": articles.getAuthor(), "body": articles.getBody(), "date": str(now)})
