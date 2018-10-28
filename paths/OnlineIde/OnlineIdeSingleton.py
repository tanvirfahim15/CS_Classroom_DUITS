from threading import Lock


class Singleton(type):
    lock = Lock()

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        Singleton.lock.acquire()
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        Singleton.lock.release()
        return cls._instance

