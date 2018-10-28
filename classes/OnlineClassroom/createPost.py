class post:

    posttext=""
    postfile=""
    author=""
    def __init__(self,posttext,postfile,author):
        self.posttext=posttext
        self.postfile=postfile
        self.author=author
    def getdescription(self):

        return self.posttext+" "+self.postfile+self.author
    def getposttext(self):
        return self.posttext
    def getpostfile(self):
        return self.postfile

    def getauthor(self):
        return self.author