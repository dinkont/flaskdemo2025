from decouple import config
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app)
app.config[
    'SQLALCHEMY_DATABASE_URI'
] = f"postgresql://{config('DB_USERNAME')}:{config('DB_PASSWORD')}@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class BookModel(db.Model):
    __tablename__ = 'books'
    pk = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    test_something = db.Column(db.String)
    reader_pk = db.Column(db.Integer, db.ForeignKey('readers.pk'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ReaderModel(db.Model):
    __tablename__ = 'readers'
    pk = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    # books = db.relationship("BookModel", backref="book", lazy='dynamic')


class BookResource(Resource):
    def post(self):
        data = request.get_json()
        reader_pk = data.pop('reader_pk')
        book = BookModel(**data)
        book.reader_pk = reader_pk
        db.session.add(book)
        db.session.commit()
        # return book.serialize(), 201
        return book.as_dict()


# f

api.add_resource(BookResource, '/books/')

if __name__ == '__main__':
    app.run()
