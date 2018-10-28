import abc
import pattern.SearchArticle.SearchFilter as Filters
from Database.database import db


class SearchContext:

    def __init__(self, strategy):
        self._strategy = strategy

    def get_articles(self):
        return self._strategy.get_articles()


class Strategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_articles(self):
        pass


class AndSearchStrategy(Strategy):

    def __init__(self, gender, institute, country, author, title):
        self.gender = gender
        self.institute = institute
        self.country = country
        self.author = author
        self.title = title

    def get_articles(self):
        articles = db.article.find()
        if self.gender == '1':
            articles = Filters.MaleFilter().and_articles(articles)
        elif self.gender == '2':
            articles = Filters.FemaleFilter().and_articles(articles)

        if self.country != '0':
            articles = Filters.CountryFilter(self.country).and_articles(articles)

        articles = Filters.ArticleTitleFilter(self.title).and_articles(articles)
        articles = Filters.InstituteFilter(self.institute).and_articles(articles)
        articles = Filters.AuthorNameFilter(self.author).and_articles(articles)
        return articles


class OrSearchStrategy(Strategy):
    def __init__(self, gender, institute, country, author, title):
        self.gender = gender
        self.institute = institute
        self.country = country
        self.author = author
        self.title = title
        if self.institute == '':
            self.institute = '#$%'
        if self.author == '':
            self.author = '#$%'
        if self.title == '':
            self.title = '#$%'

    def get_articles(self):
        articles = []
        if self.gender == '1':
            articles = Filters.MaleFilter().or_articles(articles)
        elif self.gender == '2':
            articles = Filters.FemaleFilter().or_articles(articles)

        if self.country != '0':
            articles = Filters.CountryFilter(self.country).or_articles(articles)
        articles = Filters.ArticleTitleFilter(self.title).or_articles(articles)
        articles = Filters.InstituteFilter(self.institute).or_articles(articles)
        articles = Filters.AuthorNameFilter(self.author).or_articles(articles)
        return articles

