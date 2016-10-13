from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class ModelMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        # db.session.delete(self)
        # db.session.commit()
        self.deleted = True
        self.save()
