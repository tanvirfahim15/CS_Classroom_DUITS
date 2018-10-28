from classes.management_class.ComponentPerson import ComponentPerson


class BasicStudent(ComponentPerson):
    def __init__(self):
        ComponentPerson.__init__(self)

    def getDescription(self):
        info={}
        info["Person"] = "Student"
        return info


