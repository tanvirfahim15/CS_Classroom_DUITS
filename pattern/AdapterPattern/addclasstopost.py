from Service.OnlineClassroom import ClassroomFeed as service
from classes.OnlineClassroom.assingment import assignment
from classes.OnlineClassroom.addclass import addclass
from classes.OnlineClassroom.assignmenttopostAdapter import addassignmenttAdapter
from classes.OnlineClassroom.addclasstopostAdapter import addclasspostAdapter
def addclasstopost(starttime,endtime,details,author):
    classtime = addclass(starttime, endtime, details, author)
    service.save_to_database(addclasspostAdapter(classtime))
    return 