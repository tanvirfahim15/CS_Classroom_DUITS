from classes.management_class.studentDecorator import studentDecorator


class phonenumberToppings(studentDecorator):
    number=0

    def __init__(self, number, componentperson):
        self.description = number
        self.componentperson = componentperson

    # def getDescription(self):
    #     return self.description+" "+self.componentperson.getDescription()

    def getDescription(self):
        info= self.componentperson.getDescription()
        info["Phone"]=self.description
        return info

