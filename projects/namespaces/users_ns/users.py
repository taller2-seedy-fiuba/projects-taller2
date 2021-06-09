"""Project namespace."""
from datetime import datetime
from projects.model import Project, DB, Image, Hashtag

from flask_restx import Namespace, Resource,  marshal

from flask_restx import Model, fields

from projects.namespaces.project_ns.models import new_project_model, project_get_model
from projects.namespaces.utils.project_query_params import ProjectQueryParams
from projects.namespaces.utils.mapper import from_projects_to_projectDtos


api = Namespace("Users", description="Get projects related to users.")

api.models[new_project_model.name] = new_project_model
query_params = ProjectQueryParams()
query_params.add_arguments()

@api.route('/<user_id>/projects')
@api.response(model=project_get_model, code=200, description="Projects related to User Id")
@api.param('user_id', 'The user unique identifier')
class ProjectsByUserIdResource(Resource):
    """Projects by User Id"""
    @api.doc(params={'user_id': 'An ID'})
    def get(self, user_id):
        """Filter and get project by user id"""
        projects = Project.query.filter(Project.user_id == user_id).all()
        return marshal(projects, project_get_model) , 200

