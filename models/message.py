from . import ModelMixin
from . import db


class Message(db.Model, ModelMixin):
    __tablename__ = 'messages'
    content = db.Column(db.String(1024))
    channel = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', 0)
        self.channel = form.get('channel', 0)
