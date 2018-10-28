import abc


class ArticleStrategy(metaclass=abc.ABCMeta):
    title = None
    body = None
    author = None

    @abc.abstractmethod
    def algorithm_interface(self):
        pass

    @abc.abstractmethod
    def create_article(self, title, body, author):
        pass
