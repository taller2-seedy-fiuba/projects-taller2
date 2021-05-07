"""Default namespace module."""
from datetime import datetime

from flask_restx import Namespace, Resource

from projects.model import Project, DB, Image, Hashtag, Type

from projects.namespaces.project_ns.models import new_project_model, type_model, image_model, hashtag_model

ns = Namespace("Projects", description="CRUD operations for projects.")

ns.models[new_project_model.name] = new_project_model
ns.models[image_model.name] = image_model
ns.models[hashtag_model.name] = hashtag_model
ns.models[type_model.name] = type_model


@ns.route('')
class ProjectsResource(Resource):
    @ns.doc('create_project')
    @ns.marshal_with(new_project_model)
    @ns.expect(new_project_model)
    def put(self):
        """Create a new project"""
        data = ns.payload
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

        types = []
        for type_data in data["types"]:
            new_type = Type(**type_data)
            types.append(new_type)
            DB.session.add(new_type)
        data["types"] = types

        data["end_date"] = datetime.strptime(data["end_date"], "%Y-%m-%d")


        new_project = Project(**data)
        DB.session.add(new_project)
        DB.session.commit()
        return new_project

    @ns.doc('get_projects')
    @ns.marshal_list_with(new_project_model)
    def get(self):
        """Get all projects"""

        query = Project.query 
        return query.all()