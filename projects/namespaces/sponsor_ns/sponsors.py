"""Sponsor namespace."""

from flask_restx import Namespace, Resource

from flask_restx import Model, fields, marshal
from projects.namespaces.sponsor_ns.models import sponsor_assigned_model
from projects.namespaces.project_ns.models import project_not_found_model, project_get_model
from projects.model import Project, Sponsor, DB
from projects.exceptions import ProjectNotFound, SponsorNotFound


api = Namespace("Sponsor", description="Actions related to Sponsor.")

api.models[sponsor_assigned_model.name] = sponsor_assigned_model


@api.route('/<user_id>/projects/<int:project_id>')
@api.param('project_id', 'The project unique identifier')
@api.param('user_id', 'The sponsor unique identifier')
class AssignSponsorResource(Resource):
    
    @api.doc('Assign Sponsor to Project ')
    @api.response(model=sponsor_assigned_model, code=200, description="Sponsor was assigned successfully")
    @api.response(model=project_not_found_model, code=404, description="No project by that id was found")
    def put(self, user_id, project_id):
        """Assign Sponsor to project"""
        data = api.payload
        project = Project.query.filter(Project.id == project_id).first()
        if project is None:
            raise ProjectNotFound
        sponsor = Sponsor.query.filter(Sponsor.id == user_id).first()
        if sponsor is None:
            sponsor = Sponsor(id=user_id)
        sponsor.projects.append(project)
        DB.session.add(sponsor)
        DB.session.commit()
        result = marshal(sponsor, sponsor_assigned_model)
        result['project_id'] = project.id
        return result, 200

@api.route('/<user_id>/projects')
@api.doc('Get all projects in which Sponsor is assigned.')
@api.response(model=project_get_model, code=200, description="Projects assigned to Sponsor")
@api.response(model=project_get_model, code=204, description="The Sponsor has not projects assigned")
@api.response(model=project_not_found_model, code=404, description="No Sponsor by that id was found")
@api.param('user_id', 'The Sponsor unique identifier')
class SponsorResource(Resource):

    @api.doc('Get projects in which user is Sponsor')
    def get(self, user_id):
        """Get all projects assigned to sponsor"""
        data = api.payload
        sponsor = Sponsor.query.filter(Sponsor.id == user_id).first()
        if sponsor is None:
            return marshal({'message': "No Sponsor by that id was found."}, project_not_found_model ), 404
        projects = sponsor.projects
        if not projects:
            return projects, 204
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
        return projects_final, 200


@api.errorhandler(ProjectNotFound)
def handle_ProjectNotFound(_exception):
    """Handle project not found exception."""
    return {'message': "No project by that id was found."}, 404

@api.errorhandler(SponsorNotFound)
def handle_SponsorNotFound(_exception):
    """Handle Sponsor not found exception."""
    return {'message': "No Sponsor by that id was found."}, 404





