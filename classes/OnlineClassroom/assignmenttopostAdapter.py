from classes.OnlineClassroom.createPost import post
class addassignmenttAdapter(post):


    def __init__(self,assignment):
        self.assignment=assignment


    def getposttext(self):
        return self.assignment.details+ " must be submitted by "+ self.assignment.duedate+ " before "+self.assignment.duetime


    def getpostfile(self):
        return ""


    def getauthor(self):
        return self.assignment.author


    def get_course_id(self):
        return self.assignment.course_id