class addclass:
    starttime=""
    endtime=""
    details=""
    author=""
    def __init__(self,starttime,endtime,details,author):
        self.endtime=endtime
        self.starttime=starttime
        self.details=details
        self.author=author
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
