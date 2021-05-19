"""Project namespace."""
from datetime import datetime
from projects.model import Project, DB, Image, Hashtag

from flask_restx import Namespace, Resource

from flask_restx import Model, fields

from projects.namespaces.users_ns.user_models import get_user_project_model


api = Namespace("Users", description="Get projects related to users.")

api.models[get_user_project_model.name] = get_user_project_model


@api.route('/<user_id>/projects')
@api.param('user_id', 'The user unique identifier')
class ProjectsByUserIdResource(Resource):
    """Projects by User Id"""
    @api.doc(params={'user_id': 'An ID'})
    @api.marshal_list_with(get_user_project_model)
    def get(self, user_id):
        """Filter and get project by user id"""
        query = Project.query.filter(Project.user_id == user_id).all()
        return query
