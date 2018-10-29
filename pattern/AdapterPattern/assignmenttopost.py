from Service.OnlineClassroom import ClassroomFeed as service
from classes.OnlineClassroom.assingment import assignment
from classes.OnlineClassroom.assignmenttopostAdapter import addassignmenttAdapter
def assignmenttopost(time ,date,details,author,courese_id):
    assign = assignment(time, date, details, author,courese_id)
    service.save_to_database(addassignmenttAdapter(assign))
    return
