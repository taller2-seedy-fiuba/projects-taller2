"""Project api."""
import json
from datetime import datetime
from projects.model import Project, DB, Image, Hashtag, Video

from flask_restx import Namespace, Resource, reqparse, marshal
from projects.namespaces.project_ns.models import *

from projects.namespaces.utils.project_query_params import ProjectQueryParams
from projects.namespaces.utils.mapper import from_projects_to_projectDtos

from projects.exceptions import ParamDoesNotAllowedException, ProjectNotFound

api = Namespace("Projects", description="CRUD operations for projects.")

api.models[new_project_model.name] = new_project_model
api.models[image_model.name] = image_model
api.models[video_model.name] = video_model
api.models[hashtag_model.name] = hashtag_model
api.models[project_not_found_model.name] = project_not_found_model

query_params = ProjectQueryParams()
query_params.add_arguments()



@api.route('')
class ProjectsResource(Resource):
    @api.doc('create_project')
    @api.marshal_with(created_project_model)
    @api.expect(new_project_model)
    def post(self):
        """Create a new project"""
        data = api.payload
        images = []
        for img_url in data["images"]:
            img_data = {"url": img_url}
            new_img = Image(**img_data)
            images.append(new_img)
            DB.session.add(new_img)
        data["images"] = images
        
        videos = []
        for video_url in data["videos"]:
            video_data = {"url": video_url}
            new_video = Video(**video_data)
            videos.append(new_video)
            DB.session.add(new_video)
        data["videos"] = videos

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
    @api.response(model=new_project_model, code=200, description="Used without pagination")
    @api.response(model=get_pagination_model, code=200, description="Used with pagination")
    @api.expect(query_params.projects_parser)
    def get(self):
        """Get all projects"""
        params = query_params.projects_parser.parse_args()
        query = Project.query
        if params:
            if "project_type" in params.keys():
                query = query.filter(Project.project_type == params['project_type'] )
            elif 'status' in params.keys():
                query = query.filter(Project.status == params['status'])
            elif "page" not in params.keys() and not "page_size" not in params.keys():
                raise ParamDoesNotAllowedException("Invalid param")
            if "page" in params.keys() and "page_size" in params.keys():
                page = query.paginate(page=params["page"], per_page=params["page_size"])
                projects = from_projects_to_projectDtos(marshal(page.items, created_project_model))
                data = {
                    'has_next': page.has_next,
                    'projects': projects
                    }
                return marshal(data, get_pagination_model) ,200
        result = marshal(query.all(), created_project_model)
        projects = from_projects_to_projectDtos(result)
        return marshal(projects, new_project_model) , 200
  

@api.route("/<int:project_id>")
@api.response(model=new_project_model, code=200, description="Get project by id successfully")
@api.response(model=project_not_found_model, code=404, description="No project by that id was found")
@api.param('project_id', 'The project unique identifier')
class ProjectsByProjectIdResource(Resource):
    @api.doc('get_projects_by_project_id')
    def get(self, project_id):
        """Get Project by Id"""
        result = Project.query.filter(Project.id == project_id).first()
        if not result:
            raise ProjectNotFound("No project by that id was found.") 
        project = marshal(result, created_project_model)

        return from_projects_to_projectDtos([project])


@api.errorhandler(ProjectNotFound)
@api.marshal_with(project_not_found_model, code=404)
def handle_blocked_publication_questions(error):
    """Handle project not found exception."""
    return {'message': error.message}, 404



