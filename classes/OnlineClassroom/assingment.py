class assignment:
    duetime=""
    duedate=""
    details=""
    author=""
    def __init__(self,duetime,duedate,details,author):
        self.duetime=duetime
        self.duedate=duedate
        self.details=details
        self.author=author
    def getduetime(self):
        return self.duetime
    def getduedate(self):
        return self.duedate
    def getdetails(self):
        return self.details
    def getauthor(self):
        return self.author
    def getpostfile(self):
        return ""
