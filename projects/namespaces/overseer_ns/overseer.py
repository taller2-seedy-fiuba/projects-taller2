"""Project namespace."""
from datetime import datetime
from projects.model import Project, DB, Image, Hashtag

from flask_restx import Namespace, Resource

from flask_restx import Model, fields
from projects.client.client import Client
from projects.namespaces.users_ns.user_models import get_user_project_model
from projects.namespaces.utils.project_query_params import ProjectQueryParams

project_client = Client(config.project.url(default=USER_URL))


api = Namespace("Overseer", description="Get projects assigned to Overseer.")

api.models[get_user_project_model.name] = get_user_project_model
query_params = ProjectQueryParams()
query_params.add_arguments()

@api.route('/<user_id>/projects')
@api.param('user_id', 'The user unique identifier')
@api.expect(query_params.projects_parser)
class OverseerResource(Resource):
    
    @api.doc('Assign Overseer to Project ')
    @api.marshal_with(created_project_model)
    @api.expect(overseer_assigned_model)
    def put(self):
        """Assign Overseer to project"""
        data = api.payload
        cl
        return new_project


