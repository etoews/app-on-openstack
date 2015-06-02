from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Image(db.Model):

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    href = db.Column(db.String(256), unique=True, nullable=False)

    def to_json(self):
        json = {'href': self.href}
        return json

    def __repr__(self):
        return '<Image %r>' % self.url
