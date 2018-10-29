class addclass:
    starttime=""
    endtime=""
    details=""
    author=""
    course_id=""
    def __init__(self,starttime,endtime,details,author,course_id):
        self.endtime=endtime
        self.starttime=starttime
        self.details=details
        self.author=author
        self.course_id=course_id
    def getstarttime(self):
        return self.starttime
    def getendtime(self):
        return self.endtime
    def getdetails(self):
        return self.details
    def getauthor(self):
        return self.author
    def getpostfile(self):
        return ""
    def getcourse_id(self):
        return self.course_id
