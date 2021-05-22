"""Project api."""

from datetime import datetime
from projects.model import Project, DB, Image, Hashtag

from flask_restx import Namespace, Resource, reqparse

from flask_restx import Model, fields

from projects.namespaces.project_ns.models import new_project_model, type_model, image_model, hashtag_model

from projects.namespaces.utils.project_query_params import ProjectQueryParams
api = Namespace("Projects", description="CRUD operations for projects.")

api.models[new_project_model.name] = new_project_model
api.models[image_model.name] = image_model
api.models[hashtag_model.name] = hashtag_model

query_params = ProjectQueryParams()
query_params.add_arguments()

@api.route('')
class ProjectsResource(Resource):
    @api.doc('create_project')
    @api.marshal_with(new_project_model)
    @api.expect(new_project_model)
    def post(self):
        """Create a new project"""
        data = api.payload
        images = []
        for img_data in data["images"]:
            new_img = Image(**img_data)
            images.append(new_img)
            DB.session.add(new_img)
        data["images"] = images

        hashtags = []
        for hashtag_data in data["hashtags"]:
            new_hash = Hashtag(**hashtag_data)
            hashtags.append(new_hash)
            DB.session.add(new_hash)
        data["hashtags"] = hashtags

        data["end_date"] = datetime.strptime(data["end_date"], "%Y-%m-%d")

        data["creation_date"] = datetime.strptime(data["creation_date"], "%Y-%m-%d")


        new_project = Project(**data)
        DB.session.add(new_project)
        DB.session.commit()
        return new_project

    @api.doc('get_projects')
    @api.marshal_list_with(new_project_model)
    @api.expect(query_params.projects_parser)
    def get(self):
        """Get all projects"""
        params = query_params.projects_parser.parse_args()
        query = Project.query
        for param_name, filter_op in params.items():
            query = filter_op.apply(query, Project )
        return query.all()




  

@api.route("/<int:project_id>")
@api.param('project_id', 'The project unique identifier')
class ProjectsByProjectIdResource(Resource):
    @api.doc('get_projects_by_project_id')
    @api.marshal_list_with(new_project_model)
    def get(self, project_id):
        """Get Project by Id"""

        query = Project.query.filter(Project.id == project_id).all()
        return query


