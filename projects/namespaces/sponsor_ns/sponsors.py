"""Sponsor namespace."""

import logging

from flask_restx import Namespace, Resource

from flask_restx import Model, fields, marshal
from projects.namespaces.sponsor_ns.models import sponsor_assigned_model
from projects.namespaces.project_ns.models import project_not_found_model, project_get_model
from projects.model import Project, Sponsor, DB, Location, Favorite
from projects.exceptions import ProjectNotFound, SponsorNotFound


logging.basicConfig(level=logging.INFO)

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
        api.logger.info(f"Trying to set {user_id} as sponsor in project: {project_id}")
        data = api.payload
        project = Project.query.filter(Project.id == project_id).first()
        if project is None:
            api.logger.error(f"No project was found by id: {project_id}")
            raise ProjectNotFound
        sponsor = Sponsor.query.filter(Sponsor.id == user_id).first()
        if sponsor is None:
            sponsor = Sponsor(id=user_id)
        sponsor.projects.append(project)
        DB.session.add(sponsor)
        DB.session.commit()
        result = marshal(sponsor, sponsor_assigned_model)
        result['project_id'] = project.id
        api.logger.info(f"Sponsor: {user_id} assigned to project: {project_id} successfully")
        return result, 200

@api.route('/<user_id>/projects/<int:project_id>/fav')
@api.param('project_id', 'The project unique identifier')
@api.param('user_id', 'The sponsor unique identifier')
class FavProjectResource(Resource):
    
    @api.doc('Add or remove project from favorites')
    @api.response(model=project_get_model, code=200, description="Project was added or removed from favorites")
    @api.response(model=project_not_found_model, code=404, description="No project by that id was found")
    def put(self, user_id, project_id):
        """Add or remove project from favorites"""
        api.logger.info("Trying to add or remove %s to user: %s ", {project_id}, {user_id})
        data = api.payload
        project = Project.query.filter(Project.id == project_id).first()
        if project is None:
            api.logger.error(f"No project was found by id: {project_id}")
            raise ProjectNotFound
        sponsor = Sponsor.query.filter(Sponsor.id == user_id).first()
        if sponsor is None:
            sponsor = Sponsor(id=user_id)
        if not bool(sponsor.favorites)  or project_id not in [fav.id  for fav in sponsor.favorites]:
            sponsor.favorites.append(Favorite(sponsor_id=user_id, project_id=project_id))
        else:
            for i, fav in enumerate(sponsor.favorites):
                if fav.project_id == project_id:
                    sponsor.favorites.pop(i)
        DB.session.add(sponsor)
        DB.session.commit()
        result = marshal(sponsor, sponsor_assigned_model)
        result['project_id'] = project.id
        api.logger.info(f"Sponsor: {user_id} fav project: {project_id} successfully")
        return result, 200


@api.route('/<user_id>/projects')
@api.doc('Get all projects in which Sponsor is assigned.')
@api.response(model=project_get_model, code=200, description="Projects assigned to Sponsor")
@api.response(model=project_get_model, code=204, description="The Sponsor has not projects assigned")
@api.response(model=project_not_found_model, code=404, description="No Sponsor by that id was found")
@api.param('user_id', 'The Sponsor unique identifier')
class SponsorResource(Resource):

    @api.marshal_list_with(project_get_model)
    @api.doc('Get projects in which user is Sponsor')
    def get(self, user_id):
        """Get all projects assigned to sponsor"""

        api.logger.info(f"Getting projects for sponsor: {user_id}...")
        data = api.payload
        sponsor = Sponsor.query.filter(Sponsor.id == user_id).first()
        if sponsor is None:
            api.logger.error(f"Not sponsor was found by id: {user_id}")
            return []
        projects = sponsor.projects
        if not projects:
            api.logger.info(f"Not projects assigned to sponsor: {user_id}")
            return []
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
            location = Location.query.filter(Location.project_id == project.id).first()
            projects_final[i]['location'][0]['country'] =  location.country
            projects_final[i]['location'][0]['latitude'] =  location.lat
            projects_final[i]['location'][0]['longitude'] =  location.lon            
        api.logger.info(f"Returning projects: {projects_final} for sponsor: {user_id}")                
        return projects_final, 200



@api.route('/<user_id>/favorite')
@api.doc('Get all favorite projects for user.')
@api.response(model=project_get_model, code=200, description="Fav projects for Sponsor")
@api.response(model=project_get_model, code=204, description="The Sponsor has not favorite projects ")
@api.response(model=project_not_found_model, code=204, description="No Sponsor by that id was found")
@api.param('user_id', 'The Sponsor unique identifier')
class SponsorResource(Resource):
    @api.marshal_list_with(project_get_model)
    @api.doc('Get favorite projects for Sponsor')
    def get(self, user_id):
        """Get all favorite projects """

        api.logger.info(f"Getting fav projects for sponsor: {user_id}...")
        data = api.payload
        sponsor = Sponsor.query.filter(Sponsor.id == user_id).first()
        if sponsor is None:
            api.logger.info(f"Not projects were saved as favorite by sponsor: {user_id}")
            return [] 
        favorites = sponsor.favorites
        if not favorites:
            api.logger.info(f"Not projects were saved as favorite by sponsor: {user_id}")
            return []
        projects_id = [fav.project_id for fav in favorites]
        api.logger.info(f"Ids for favorite projects found for sponsor: {user_id} are: {projects_id}")                
        projects_final = []
        projects = []
        for project_id in projects_id:
            projects.append(Project.query.filter(Project.id == project_id).first())
        api.logger.info(f"Favorite projects found for sponsor: {user_id} are: {projects}")                
        for i, project in enumerate(projects):
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
            location = Location.query.filter(Location.project_id == project.id).first()
            projects_final[i]['location'][0]['country'] =  location.country
            projects_final[i]['location'][0]['latitude'] =  location.lat
            projects_final[i]['location'][0]['longitude'] =  location.lon            
        api.logger.info(f"Returning fav projects: {projects_final} for sponsor: {user_id}")                
        return projects_final, 200





