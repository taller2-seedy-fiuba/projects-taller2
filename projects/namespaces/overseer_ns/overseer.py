"""Overseer namespace."""

import logging
from flask_restx import Namespace, Resource

from flask_restx import Model, fields, marshal
from projects.namespaces.overseer_ns.models import assign_overseer_model, overseer_assigned_model
from projects.namespaces.project_ns.models import project_not_found_model, project_get_model
from projects.model import Project, Overseer, DB, AssignedStatus, Location
from projects.exceptions import ProjectNotFound, OverseerNotFound


logging.basicConfig(level=logging.INFO)

api = Namespace("Overseer", description="Get projects assigned to Overseer.")

api.models[overseer_assigned_model.name] = overseer_assigned_model
api.models[assign_overseer_model.name] = assign_overseer_model


@api.route('/<user_id>/projects/<int:project_id>')
@api.param('project_id', 'The project unique identifier')
@api.param('user_id', 'The overseer unique identifier')
class AssignOverseerResource(Resource):
    
    @api.doc('Assign Overseer to Project ')
    @api.response(model=overseer_assigned_model, code=200, description="Overseer was assigned successfully")
    @api.response(model=project_not_found_model, code=404, description="No project by that id was found")
    @api.expect(assign_overseer_model)
    def put(self, user_id, project_id):
        """Assign Overseer to project"""
        data = api.payload
        project = Project.query.filter(Project.id == project_id).first()
        if project is None:
            api.logger.info(f"Project not found by id: {project_id}")
            raise ProjectNotFound
        overseer = Overseer.query.filter(Overseer.id == user_id).first()
        if overseer is None:
            overseer = Overseer(id=user_id)
        if data["confirmed"]:
            overseer.confirmed = True
            overseer.assigned_status = AssignedStatus.confirmed
            overseer.projects.append(project)
        else:
            overseer.assigned_status = AssignedStatus.rejected
        DB.session.add(overseer)
        DB.session.commit()
        api.logger.info(f"Status: {overseer.assigned_status} confirmed")
        return marshal(overseer, overseer_assigned_model), 200

@api.route('/<user_id>/projects')
@api.doc('Get all projects in which Overseer is assigned.')
@api.response(model=project_get_model, code=200, description="Projects assigned to overseer")
@api.response(model=project_get_model, code=204, description="The overseer has not projects assigned")
@api.response(model=project_get_model, code=404, description="No Oversser by that id was found")
@api.param('user_id', 'The overseer unique identifier')
class OverseerResource(Resource):

    @api.marshal_list_with(project_get_model)
    @api.doc('Get projects in which user is Overseer')
    def get(self, user_id):
        """Get all projects assigned to overseer"""
        data = api.payload
        overseer = Overseer.query.filter(Overseer.id == user_id).first()
        if not bool(overseer):
            api.logger.info(f"Not projects assigned to overseer: {user_id}")
            return marshal([], project_get_model) , 204
        projects = overseer.projects
        if not bool(projects):
            api.logger.info(f"Not projects assigned to overseer: {user_id}")
            return marshal([], project_get_model) , 204
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
        api.logger.info(f"Getting projects: {projects_final} for overseer: {user_id}")

        return marshal(projects_final, project_get_model) , 200


@api.errorhandler(ProjectNotFound)
def handle_ProjectNotFound(_exception):
    """Handle project not found exception."""
    return {'message': "No project by that id was found."}, 404

@api.errorhandler(OverseerNotFound)
def handle_ProjectNotFound(_exception):
    """Handle Overseer not found exception."""
    return {'message': "No overseer by that id was found."}, 404





