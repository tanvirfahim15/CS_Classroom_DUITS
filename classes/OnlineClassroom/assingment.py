class assignment:
    duetime=""
    duedate=""
    details=""
    author=""
    course_id=""
    def __init__(self,duetime,duedate,details,author,course_id):
        self.duetime=duetime
        self.duedate=duedate
        self.details=details
        self.author=author
        self.course_id=course_id
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
    def getcourse_id(self):
        return self.course_id
