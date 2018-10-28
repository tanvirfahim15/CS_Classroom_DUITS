
class Subject:
    def register_observer(self, observer):
        pass

    def remove_observer(self, observer):
        pass

    def notify_observer(self):
        pass


class Observer:
    def update(self, message):
        pass
