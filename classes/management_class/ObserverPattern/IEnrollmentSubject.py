import abc


class IEnrollmentSubject(metaclass=abc.ABCMeta):
    """
    Define an updating interface for objects that should be notified of
    changes in a subject.
    """

    def __init__(self):
        self._subject = None
        self._observer_state = None



    @abc.abstractmethod
    def registerObserver(self,Observer):
        pass

    @abc.abstractmethod
    def removeObserver(self,Observer):
        pass

    @abc.abstractmethod
    def notifyObserver(self):
        pass
