from Service.OnlineClassroom import ClassroomFeed as service
from classes.OnlineClassroom.addclass import addclass
from classes.OnlineClassroom.addclasstopostAdapter import addclasspostAdapter
def addclasstopost(starttime,endtime,details,author,course_id):
    classtime = addclass(starttime, endtime, details, author,course_id)
    service.save_to_database(addclasspostAdapter(classtime))
    return 