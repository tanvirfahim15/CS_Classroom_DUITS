import abc
from Database.database import db


class Filter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def and_articles(self, articles):
        pass

    def or_articles(self, articles):
        result = articles
        for article in self.and_articles(db.article.find()):
            if article not in result:
                result.append(article)
        return result


class MaleFilter(Filter):

    def and_articles(self, articles):
        users = []
        for user in db.users.find():
            if 'gender' in user.keys() and user['gender'] == '1':
                users.append(user['username'])

        result = []
        for article in articles:
            if article['author'] in users:
                result.append(article)
        return result


class FemaleFilter(Filter):

    def and_articles(self, articles):
        users = []
        for user in db.users.find():
            if 'gender' in user.keys() and user['gender'] == '2':
                users.append(user['username'])

        result = []
        for article in articles:
            if article['author'] in users:
                result.append(article)
        return result


class InstituteFilter(Filter):

    def __init__(self, institute):
        self.institute = institute

    def and_articles(self, articles):
        users = []
        for user in db.users.find():
            if 'institute' in user.keys() and self.institute.lower() in user['institute'].lower():
                users.append(user['username'])

        result = []
        for article in articles:
            if article['author'] in users:
                result.append(article)
        return result


class CountryFilter(Filter):

    def __init__(self, country):
        self.country = country

    def and_articles(self, articles):
        users = []
        for user in db.users.find():
            if 'country' in user.keys() and self.country in user['country']:
                users.append(user['username'])

        result = []
        for article in articles:
            if article['author'] in users:
                result.append(article)
        return result


class AuthorNameFilter(Filter):

    def __init__(self, author):
        self.author = author

    def and_articles(self, articles):

        result = []
        for article in articles:
            if self.author in article['author']:
                result.append(article)
        return result


class ArticleTitleFilter(Filter):

    def __init__(self, title):
        self.title = title

    def and_articles(self, articles):

        result = []
        for article in articles:
            if self.title.lower() in article['title'].lower():
                result.append(article)
        return result


