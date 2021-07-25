from flask import Flask
from flask_restful import Api, Resource, reqparse, inputs
import sys

app = Flask(__name__)

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


class WebCalendarResource(Resource):
    def get(self):
        return {'data': 'There are no events for today!'}


class EventResource(Resource):
    def post(self):
        args = eventParser.parse_args()
        if 'message' in args:
            return {'message': args['message']}
        return {'message': 'The event has been added!', 'event': args['event'], 'date': str(args['date'].date())}


api.add_resource(WebCalendarResource, '/event/today')
api.add_resource(EventResource, '/event')


# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
