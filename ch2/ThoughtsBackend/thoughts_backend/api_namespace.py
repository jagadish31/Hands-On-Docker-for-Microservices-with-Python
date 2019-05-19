import http.client
from datetime import datetime
from flask_restplus import Namespace, Resource, fields
from thoughts_backend.models import ThoughtModel
from thoughts_backend.db import db

api_namespace = Namespace('api', description='API operations')


# Input and output formats for Thought
thought_parser = api_namespace.parser()
thought_parser.add_argument('username', type=str, required=True,
                            help='User creating the thought')
thought_parser.add_argument('text', type=str, required=True,
                            help='Text of the thought')

model = {
    'id': fields.Integer(),
    'username': fields.String(),
    'text': fields.String(),
    'timestamp': fields.DateTime(),
}
thought_model = api_namespace.model('Thought', model)


@api_namespace.route('/thoughts/')
class ThoughtListCreate(Resource):

    @api_namespace.doc('list_thoughts')
    @api_namespace.marshal_with(thought_model)
    def get(self):
        '''
        Retrieves all the thoughts
        '''
        thoughts = ThoughtModel.query.order_by('id').all()
        return thoughts

    @api_namespace.doc('create_thoughts')
    @api_namespace.expect(thought_parser)
    def post(self):
        '''
        Create a new thought
        '''
        args = thought_parser.parse_args()

        new_thought = ThoughtModel(username=args['username'],
                                   text=args['text'],
                                   timestamp=datetime.utcnow())
        db.session.add(new_thought)
        db.session.commit()

        result = api_namespace.marshal(new_thought, thought_model)

        return result, http.client.CREATED


@api_namespace.route('/thoughts/<int:thought_id>')
class ThoughtsRetrieve(Resource):

    @api_namespace.doc('retrieve_thought')
    @api_namespace.marshal_with(thought_model)
    def get(self, thought_id):
        '''
        Retrieve a thought
        '''
        thought = ThoughtModel.query.get(thought_id)
        if not thought:
            # The thought is not present
            return '', http.client.NOT_FOUND

        return thought
