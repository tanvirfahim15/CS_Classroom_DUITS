from classes.management_class.studentDecorator import studentDecorator


class genderToppings(studentDecorator):
    gender=""

    def __init__(self, gender, componentperson):
        # super().__init__()
        self.description = gender
        self.componentperson = componentperson;

    # def getDescription(self):
    #     return self.description+" "+self.componentperson.getDescription()
    #
    def getDescription(self):
        info= self.componentperson.getDescription()
        # print("In GenderTop")
        # print(info)
        info["Gender"]=self.description
        # print(info)
        return info

