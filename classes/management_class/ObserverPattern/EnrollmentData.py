from classes.management_class.ObserverPattern.IEnrollmentSubject import IEnrollmentSubject


class EnrollmentData(IEnrollmentSubject):

    observers=[]
    studentEnroll={}
    techerEnroll={}

    def __init__(self):
        pass


    def registerObserver(self,Observer):
        self.observers.append(Observer)


    def removeObserver(self,Observer):
        self.observers.remove(Observer)

    def notifyObserver(self):
        for obs in self.observers:
            obs.update(self.studentEnroll, self.techerEnroll)


    def requestPending(self):
        self.notifyObserver()


    def putStudentRequest(self, studentInfo):
        self.studentEnroll=studentInfo
        self.requestPending()

    def putTeacherRequest(self,teacherInfo):
        self.techerEnroll=teacherInfo
        self.requestPending()



