import pattern.ObserverPattern as ObserverPattern
from Database.database import db
import classes.Blog.Subscription.MailReciever as MailReciever


class Writer(ObserverPattern.Subject):
    writer_id = ""

    def __init__(self, writer):
        self.writer_id = writer

    def find_observer(self, observer):
        writer = db.subsription.find_one({'writer_id': self.writer_id})
        if writer is None:
            return False
        elif observer not in writer['readers']:
            return False
        return True

    def register_observer(self, observer):
        writer = db.subsription.find_one({'writer_id': self.writer_id})
        if writer is None:
            writer = dict()
            writer['readers'] = [observer]
            writer['writer_id'] = self.writer_id
            db.subsription.insert_one(writer)
        else:
            if observer not in writer['readers']:
                writer['readers'].append(observer)
            db.subsription.replace_one({'writer_id': self.writer_id}, writer)

    def remove_observer(self, observer):
        writer = db.subsription.find_one({'writer_id': self.writer_id})
        if writer is None:
            return
        else:
            writer['readers'].remove(observer)
            db.subsription.replace_one({'writer_id': self.writer_id}, writer)

    def notify_observer(self, article_id):
        writer = db.subsription.find_one({'writer_id': self.writer_id})
        for reader in writer['readers']:
            MailReciever.MailReciever(reader).update((self.writer_id, article_id))

