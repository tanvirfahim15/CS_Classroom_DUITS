class post:

    posttext=""
    postfile=""
    author=""
    course_id=""

    def __init__(self,posttext,postfile,author,course_id):
        self.posttext=posttext
        self.postfile=postfile
        self.author=author
        self.course_id = course_id

    def getdescription(self):

        return self.posttext+" "+self.postfile+self.author


    def getposttext(self):
        return self.posttext
    def getpostfile(self):
        return self.postfile

    def getauthor(self):
        return self.author

    def get_course_id(self):
        return self.course_id