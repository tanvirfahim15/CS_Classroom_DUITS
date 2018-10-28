from classes.management_class.studentDecorator import studentDecorator


class nameToppings(studentDecorator):


    def __init__(self, name, componentperson):
        self.description = name
        self.componentperson = componentperson

    # def getDescription(self):
    #     return self.description+" "+self.componentperson.getDescription()

    def getDescription(self):
        info= self.componentperson.getDescription()
        # print("In NameTop")
        # print(info)
        info["Name"]=self.description
        # print(info)
        return info