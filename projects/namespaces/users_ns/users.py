"""Project namespace."""
from datetime import datetime
from projects.model import Project, DB, Image, Hashtag, Location

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
    @api.marshal_list_with(project_get_model)
    @api.doc(params={'user_id': 'An ID'})
    def get(self, user_id):
        """Filter and get project by user id"""
        projects = Project.query.filter(Project.user_id == user_id).all()
        result = marshal(projects, project_get_model)
        projects_final = []
        for project in projects:
            url_images = []
            for image in project.images:
                url_images.append(image.url)
            project_dto = marshal(project, project_get_model)
            project_dto['images'] = url_images
            projects_final.append(project_dto)
        for i, project in enumerate(projects):
            url_videos = []
            for video in project.videos:
                url_videos.append(video.url)
            projects_final[i]['videos'] = url_videos
        for i, project in enumerate(projects):
            hashtags = []
            for hashtag in project.hashtags:
                hashtags.append(hashtag.name)
            projects_final[i]['hashtags'] = hashtags
        for i, project in enumerate(projects):
            overseers = []
            for overseer in project.overseers:
                overseers.append(overseer.id)
            projects_final[i]['overseers'] = overseers  
        for i, project in enumerate(projects):
            sponsors = []
            for sponsor in project.sponsors:
                sponsors.append(sponsor.id)
            projects_final[i]['sponsors'] = sponsors 
        for i, project in enumerate(projects):
            projects_final[i]['project_status'] = project.project_status.name     
        for i, project in enumerate(projects):
            location = Location.query.filter(Location.project_id == project.id).first()
            projects_final[i]['location'][0]['country'] =  location.country
            projects_final[i]['location'][0]['latitude'] =  location.lat
            projects_final[i]['location'][0]['longitude'] =  location.lon                                 
        return projects_final , 200

