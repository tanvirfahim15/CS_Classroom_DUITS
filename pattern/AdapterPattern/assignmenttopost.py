from Service.OnlineClassroom import ClassroomFeed as service
from classes.OnlineClassroom.assingment import assignment
from classes.OnlineClassroom.addclass import addclass
from classes.OnlineClassroom.assignmenttopostAdapter import addassignmenttAdapter
from classes.OnlineClassroom.addclasstopostAdapter import addclasspostAdapter
def assignmenttopost(time ,date,details,author):
    assign = assignment(time, date, details, author)
    service.save_to_database(addassignmenttAdapter(assign))
    return
