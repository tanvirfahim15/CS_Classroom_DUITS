# Python 3.4+
from classes.management_class.ComponentPerson import ComponentPerson

from abc import ABCMeta
import  six
@six.add_metaclass(ABCMeta)
class studentDecorator(ComponentPerson):

    def __init__(self):
        componentperson = ComponentPerson()

    def getDescription(self):
        return ""


# # Python 3.0+
# from abc import ABCMeta, abstractmethod
# class Abstract(metaclass=ABCMeta):
#     @abstractmethod
#     def foo(self):
#         pass
#
# # Python 2
# from abc import ABCMeta, abstractmethod
# class Abstract:
#     __metaclass__ = ABCMeta
#
#     @abstractmethod
#     def foo(self):
#         pass


