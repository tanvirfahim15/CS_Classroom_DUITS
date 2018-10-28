import abc
from Database.database import db
from bson import ObjectId
from pattern.SendNotifications import NotificationReceiver


class Subject(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def register_observer(self, observer):
        pass

    @abc.abstractmethod
    def remove_observer(self, observer):
        pass

    @abc.abstractmethod
    def notify_observer(self):
        pass


class Sender(Subject):
    course_id =""
    notifications =""

    def __init__(self , course_id , notifications):
        self.course_id = course_id
        self.notifications = notifications

    def register_observer(self, observer):
        course = db.courses.find_one({'_id': ObjectId(self.course_id)})
        course['enrolled'].append(observer)
        db.courses.replace_one({'_id': ObjectId(self.course_id)},course)
        return

    def remove_observer(self, observer):
        course = db.courses.find_one({'_id': ObjectId(self.course_id)})
        course['enrolled'].remove(observer)
        db.courses.replace_one({'_id': ObjectId(self.course_id)}, course)
        return

    def notify_observer(self):
        course = db.courses.find_one({'_id': ObjectId(self.course_id)})
        for user in course['enrolled']:
            NotificationReceiver.Receiver(user, self.notifications).update()
        return
