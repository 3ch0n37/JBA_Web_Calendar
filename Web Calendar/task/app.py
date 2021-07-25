import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, inputs, fields, marshal_with
import sys

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'

# write your code here
api = Api(app)
eventParser = reqparse.RequestParser()
eventParser.add_argument(
    'event',
    type=str,
    help='The event name is required!',
    required=True
)
eventParser.add_argument(
    'date',
    type=inputs.date,
    help='The event date with the correct format is required! The correct format is YYYY-MM-DD!',
    required=True
)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)


event_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.String
}


class WebCalendarResource(Resource):
    @marshal_with(event_fields)
    def get(self):
        events = Event.query.filter(Event.date == datetime.date.today()).all()
        if events is None:
            return {'data': 'There are no events for today!'}
        else:
            return events


class EventResource(Resource):
    def post(self):
        args = eventParser.parse_args()
        if 'message' in args:
            return {'message': args['message']}
        ev = Event(event=args['event'], date=args['date'])
        db.session.add(ev)
        db.session.commit()
        return {'message': 'The event has been added!', 'event': args['event'], 'date': str(args['date'].date())}

    @marshal_with(event_fields)
    def get(self):
        return Event.query.all()


db.create_all()
api.add_resource(WebCalendarResource, '/event/today')
api.add_resource(EventResource, '/event')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
