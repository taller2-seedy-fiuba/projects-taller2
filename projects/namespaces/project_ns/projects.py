"""Project namespace."""
from datetime import datetime
from projects.model import Project, DB, Image, Hashtag

from flask_restx import Namespace, Resource

from flask_restx import Model, fields

from projects.namespaces.project_ns.models import new_project_model, type_model, image_model, hashtag_model


api = Namespace("Projects", description="CRUD operations for projects.")

api.models[new_project_model.name] = new_project_model
api.models[image_model.name] = image_model
api.models[hashtag_model.name] = hashtag_model

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


        new_project = Project(**data)
        DB.session.add(new_project)
        DB.session.commit()
        return new_project

    @api.doc('get_projects')
    @api.marshal_list_with(new_project_model)
    def get(self):
        """Get all projects"""

        query = Project.query 
        return query.all()

@api.route('/<user_id>')
@api.param('user_id', 'The user unique identifier')
class ProjectsByUserIdResource(Resource):
    """Projects by User Id"""
    @api.doc(params={'user_id': 'An ID'})
    @api.marshal_list_with(new_project_model)
    def get(self, user_id):
        """Filter and get project by user id"""
        query = Project.query.filter(Project.user_id == user_id).all()
        return query


@api.route("/<int:project_id>")
@api.param('project_id', 'The project unique identifier')
class ProjectsByProjectIdResource(Resource):
    """Projects by Id"""
    @api.doc('get_projects_by_project_id')
    @api.marshal_list_with(new_project_model)
    def get(self, project_id):
        """Get all projects"""

        query = Project.query.filter(Project.id == project_id).all()
        return query