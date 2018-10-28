from paths.Blog import ArticleStrategy

class Context:
    title = ""
    body = ""
    author = ""

    def __init__(self, strategy):
        self._strategy = strategy

    def context_interface(self):
        self._strategy.algorithm_interface()

    def getTitle(self):
        return self.title

    def getBody(self):
        return self.body

    def getAuthor(self):
        return self.author

    def setTitle(self, title):
        self.title = title

    def setBody(self, body):
        self.body = body

    def setAuthor(self, author):
        self.author = author

class BlogArticleConcreteStrategy(ArticleStrategy.ArticleStrategy):
    title = ""
    body = ""
    author = ""

    def algorithm_interface(self):
        pass

    def BlogArticleConcreteStrategy(self):
        pass

    def create_article(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author

    def getTitle(self):
        return self.title

    def getBody(self):
        return self.body

    def getAuthor(self):
        return self.author

    def setTitle(self, title):
        self.title = title

    def setBody(self, body):
        self.body = body

    def setAuthor(self, author):
        self.author = author