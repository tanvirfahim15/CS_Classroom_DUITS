from classes.management_class.studentDecorator import studentDecorator


class passwordToppings(studentDecorator):
    password = ""

    def __init__(self, password, componentperson):
        self.description = password
        self.componentperson = componentperson;


    # def getDescription(self):
    #     return self.description+" "+self.componentperson.getDescription()


    def getDescription(self):
        info= self.componentperson.getDescription()
        info["Password"]=self.description
        return info


