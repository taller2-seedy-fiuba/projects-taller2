"""Project api."""
import json
import logging
from datetime import datetime
from sqlalchemy import func
from projects.model import Project, DB, Image, Hashtag, Video, Stage, ProjectStatus, Location, Overseer

from flask_restx import Namespace, Resource, reqparse, marshal
from projects.namespaces.project_ns.models import *

from projects.namespaces.utils.project_query_params import ProjectQueryParams
from projects.exceptions import ParamDoesNotAllowedException, ProjectNotFound, OverseerNotFound

from projects.exceptions import ParamDoesNotAllowedException, ProjectNotFound

logging.basicConfig(level=logging.INFO)

api = Namespace("Projects", description="CRUD operations for projects.")

api.models[new_project_model.name] = new_project_model
api.models[project_get_model.name] = project_get_model
api.models[project_get_pagination_model.name] = project_get_pagination_model
api.models[image_model.name] = image_model
api.models[video_model.name] = video_model
api.models[hashtag_model.name] = hashtag_model
api.models[project_not_found_model.name] = project_not_found_model
api.models[new_stage_model.name] = new_stage_model
api.models[location_model.name] = location_model
api.models[user_new_project_model.name] = user_new_project_model
api.models[stages_updated_model.name] = stages_updated_model
api.models[update_stage_model.name] = update_stage_model
api.models[update_status_model.name] = update_status_model

query_params = ProjectQueryParams()
query_params.add_arguments()



@api.route('')
class ProjectsResource(Resource):
    @api.doc('create_project')
    @api.marshal_with(project_get_model)
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
        for hashtag in data["hashtags"]:
            hashtag_data = {"name": hashtag}
            new_hash = Hashtag(**hashtag_data)
            hashtags.append(new_hash)
            DB.session.add(new_hash)
        data["hashtags"] = hashtags

        data["end_date"] = datetime.strptime(data["end_date"], "%Y-%m-%d")

        data["creation_date"] = datetime.strptime(data["creation_date"], "%Y-%m-%d")

        stages = []
        for stage in data["stages"]:
            new_stage = Stage(**stage)
            stages.append(new_stage)
            DB.session.add(new_stage)

        data['stages'] = stages
        point = f"POINT({data['location']['latitude']} {data['location']['longitude']})"
        location_data = {
            'country' : data['location']['country'],
            'point': point,
            'lat': data['location']['latitude'],
            'lon' : data['location']['longitude'],
        }
        location = Location(**location_data)
        data['location'] = [location]
        DB.session.add(location)

        overseers = []
        overseer: int
        for overseer_id in data["overseers"]:
            overseer = Overseer.query.filter(Overseer.id == overseer_id).first()
            if overseer is None:
                overseer = Overseer(id=overseer_id)
            overseers.append(overseer)
            DB.session.add(overseer)
        data['overseers'] = overseers
        data['status'] = ProjectStatus.pending.name

        new_project = Project(**data)
        DB.session.add(new_project)
        DB.session.commit()
        api.logger.info(f"Project created successfully")
        result = marshal(new_project, project_get_model)
        images_url = []
        for image in new_project.images:
            images_url.append(image.url)
        videos_url = []
        for video in new_project.videos:
            videos_url.append(video.url)
        hashtags_name = []
        for hashtag in new_project.hashtags:
            hashtags_name.append(hashtag.name)
        overseer_ids = []
        for overseer in new_project.overseers:
            overseer_ids.append(overseer.id)
        sponsors_ids = []
        for sponsor in new_project.sponsors:
            sponsors_ids.append(sponsor.id)                        
        result['images'] = images_url
        result['videos'] = videos_url
        result['hashtags'] = hashtags_name
        result['overseers'] = overseer_ids
        result['sponsors'] = sponsors_ids
        location = Location.query.filter(Location.project_id == new_project.id).first()
        result['location'][0]['country'] =  location.country
        result['location'][0]['latitude'] =  location.lat
        result['location'][0]['longitude'] =  location.lon
        result['project_status'] =  new_project.project_status.name
        return result


    @api.doc('get_projects')
    @api.response(model=project_get_model, code=200, description="Used without pagination")
    @api.response(model=project_get_pagination_model, code=200, description="Used with pagination")
    @api.expect(query_params.projects_parser)
    def get(self):
        """Get all projects"""
        params = query_params.projects_parser.parse_args()
        query = Project.query
        if params:
            if "project_type" in params.keys():
                query = query.filter( func.lower(Project.project_type) ==  func.lower(params['project_type']))
            elif 'project_status' in params.keys():
                query = query.filter(Project.project_status == params['project_status'])
            elif 'hashtag' in params.keys():
                projects = []
                hashtags = Hashtag.query.filter(func.lower(Hashtag.name) == func.lower(params['hashtag']))
                for hashtag in hashtags:
                    projects.append(query.filter(Project.id == hashtag.project_id).first())
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
                    url_hashtags = []
                    for hashtag in project.hashtags:
                        url_hashtags.append(hashtag.name)
                    projects_final[i]['hashtags'] = url_hashtags     
                for i, project in enumerate(projects):
                    overseer_ids = []
                    for overseer in project.overseers:
                        overseer_ids.append(overseer.id)
                    projects_final[i]['overseers'] = overseer_ids
                for i, project in enumerate(projects):
                    sponsors = []
                    for sponsor in project.sponsors:
                        sponsors.append(sponsor.id)
                    projects_final[i]['sponsors'] = sponsors 
                for i, project in enumerate(projects):
                    for status in project.sponsors:
                        sponsors.append(sponsor.id)
                        projects_final[i]['sponsors'] = sponsors
                for i, project in enumerate(projects):
                    projects_final[i]['project_status'] = project.project_status.name                     
                api.logger.info(f"Getting projects: {projects_final}")
                for i, project in enumerate(projects):
                    location = Location.query.filter(Location.project_id == project.id).first()
                    projects_final[i]['location'][0]['country'] =  location.country
                    projects_final[i]['location'][0]['latitude'] =  location.lat
                    projects_final[i]['location'][0]['longitude'] =  location.lon                   
                api.logger.info(f"Getting projects: {projects_final}")      
                return marshal(projects_final, project_get_model) , 200
            elif 'center_x' in params.keys() and 'center_y' in params.keys() and 'radius' in params.keys():
                center = func.ST_GeographyFromText(
                    f"POINT({params['center_x']} {params['center_y']})", srid=4326
                )
                projects = query.filter(
                    func.ST_DWithin(Location.point, center, params['radius'])
                ).all()
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
                    url_hashtags = []
                    for hashtag in project.hashtags:
                        url_hashtags.append(hashtag.name)
                        projects_final[i]['hashtags'] = url_hashtags 
                for i, project in enumerate(projects):
                    projects_final[i]['project_status'] = project.project_status.name   
                for i, project in enumerate(projects):
                    location = Location.query.filter(Location.project_id == project.id).first()
                    projects_final[i]['location'][0]['country'] =  location.country
                    projects_final[i]['location'][0]['latitude'] =  location.lat
                    projects_final[i]['location'][0]['longitude'] =  location.lon                           
                return marshal(projects_final, project_get_model) , 200            
            elif "page" not in params.keys() and not "page_size" not in params.keys():
                raise ParamDoesNotAllowedException("Invalid param")
            if "page" in params.keys() and "page_size" in params.keys():
                page = query.paginate(page=params["page"], per_page=params["page_size"])
                projects = page.items
                projects_images =[]
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
                    projects_final[i]['project_status'] = project.project_status.name                    
                for i, project in enumerate(projects):
                    url_hashtags = []
                    for hashtag in project.hashtags:
                        url_hashtags.append(hashtag.name)
                        projects_final[i]['hashtags'] = url_hashtags
                for i, project in enumerate(projects):
                    location = Location.query.filter(Location.project_id == project.id).first()
                    projects_final[i]['location'][0]['country'] =  location.country
                    projects_final[i]['location'][0]['latitude'] =  location.lat
                    projects_final[i]['location'][0]['longitude'] =  location.lon                    
                data = {
                    'has_next': page.has_next,
                    'projects': projects_final
                    }
                return marshal(data, project_get_pagination_model) ,200
        projects = query.all()
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
            url_hashtags = []
            for hashtag in project.hashtags:
                url_hashtags.append(hashtag.name)
            projects_final[i]['hashtags'] = url_hashtags     
        for i, project in enumerate(projects):
            overseer_ids = []
            for overseer in project.overseers:
                overseer_ids.append(overseer.id)
            projects_final[i]['overseers'] = overseer_ids
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
        api.logger.info(f"Getting projects: {projects_final}")   
        return marshal(projects_final, project_get_model) , 200

  

@api.route("/<int:project_id>")
@api.response(model=project_get_model, code=200, description="Get project by id successfully")
@api.response(model=project_not_found_model, code=404, description="No project by that id was found")
@api.param('project_id', 'The project unique identifier')
class ProjectsByProjectIdResource(Resource):
    @api.doc('get_projects_by_project_id')
    def get(self, project_id):
        """Get Project by Id"""
        result = Project.query.filter(Project.id == project_id).first()
        if not result:
            api.logger.info(f"No project by id {project_id}")
            return marshal({'message': "No project by that id was found."}, project_not_found_model), 404
        project = marshal(result, project_get_model)
        images_url = []
        for image in result.images:
            images_url.append(image.url)
        videos_url = []
        for video in result.videos:
            videos_url.append(video.url)
        hashtags_name = []
        for hashtag in result.hashtags:
            hashtags_name.append(hashtag.name)
        overseer_ids = []
        for overseer in result.overseers:
            overseer_ids.append(overseer.id)
        sponsors_ids = []
        for sponsor in result.sponsors:
            sponsors_ids.append(sponsor.id)                        
        project['images'] = images_url
        project['videos'] = videos_url
        project['hashtags'] = hashtags_name
        project['overseers'] = overseer_ids
        project['sponsors'] = sponsors_ids
        location = Location.query.filter(Location.project_id == result.id).first()
        project['location'][0]['country'] =  location.country
        project['location'][0]['latitude'] =  location.lat
        project['location'][0]['longitude'] =  location.lon
        project['project_status'] =  result.project_status.name
        api.logger.info(f"Getting project: {project}")
        return  marshal(project, project_get_model) , 200

    @api.response(model=project_get_model, code=200, description="Get project by id successfully")
    @api.response(model=project_not_found_model, code=404, description="No project by that id was found")
    @api.expect(user_new_project_model)
    def put(self, project_id):
            project = Project.query.filter(Project.id == project_id).first()
            if not project:
                return marshal({'message': "No project by that id was found."}, project_not_found_model), 404
            data = api.payload

            project.title = data['title']
            project.description = data['description']

            project.end_date = datetime.strptime(data["end_date"], "%Y-%m-%d")
            point = f"POINT({data['location']['latitude']} {data['location']['longitude']})"
            location_data = {
                'country' : data['location']['country'],
                'point': point
            }
            location = Location(**location_data)
            data['location'] = [location]
            DB.session.add(location)
            project.project_status = data['project_status'] 

            for image in project.images:
                DB.session.delete(image)

            images = []
            for img_url in data["images"]:
                img_data = {
                    "url": img_url,
                    "project_id": project.id
                }
                new_img = Image(**img_data)
                images.append(new_img)
                DB.session.add(new_img)
            data["images"] = images
            project.images = images

            for video in project.videos:
                DB.session.delete(video)

            videos = []
            for video_url in data["videos"]:
                video_data = {
                    "url": video_url,
                    "project_id": project.id
                }
                new_video = Video(**video_data)
                videos.append(new_video)
                DB.session.add(new_video)
            data["videos"] = videos
            project.videos = videos

            for hashtag in project.hashtags:
                DB.session.delete(hashtag)

            hashtags = []
            for hashtag in data["hashtags"]:
                hashtag = {
                    "name": hashtag,
                    "project_id": project.id
                }
                new_hashtag = Hashtag(**hashtag)
                hashtags.append(new_hashtag)
                DB.session.add(new_hashtag)
            data["hashtags"] = hashtags
            project.hashtags = hashtags


            stages = []
            for stage in data["stages"]:
                stage = {
                    "name": stage['name'],
                    "project_id": project.id,
                    "status" : ProjectStatus.pending,
                    "budget" : stage['budget'],
                    "number" : stage['number']
                }
                new_stage = Stage(**stage)
                stages.append(new_stage)
                DB.session.add(new_stage)
            data["stages"] = stages
            project.stages = stages


            DB.session.add(project)
            DB.session.commit()
            result = marshal(project, project_get_model)
            images_url = []
            for image in project.images:
                images_url.append(image.url)
            videos_url = []
            for video in project.videos:
                videos_url.append(video.url)
            hashtag_url = []
            for hashtag in project.hashtags:
                hashtag_url.append(hashtag.name)
            result['hashtags'] = images_url    
            result['images'] = images_url
            result['videos'] = videos_url
            api.logger.info(f"Project: {project_id} updated")
            return result, 200    

           
@api.route("/<int:project_id>/stage/<int:stage_number>")
@api.response(model=project_get_model, code=200, description="Status of stage updated successfully")
@api.response(model=project_not_found_model, code=404, description="No project by that id was found")
@api.param('project_id', 'The project unique identifier')
@api.param('stage_number', 'The number of stage to be updated')
class UpdateStageResource(Resource):
    @api.expect(update_stage_model)
    @api.doc('Update stages of project')
    def patch(self, project_id, stage_number):
        """Update stages"""
        data = api.payload
        result = Project.query.filter(Project.id == project_id).first()
        if not result:
            api.logger.info(f"No project by id {project_id}")
            return marshal({'message': "No project by that id was found."}, project_not_found_model), 404
        stages = result.stages 
        for stage in stages:
            if stage.number == stage_number:
                stage.status = data["status"]
                DB.session.add(stage)
                DB.session.commit()
        result = marshal(stages, stage_updated_model)
        for i, stage in enumerate(stages):      
            result[i]['status'] = stage.status.name
        return result , 200

@api.route("/<int:project_id>/status")
@api.response(model=project_get_model, code=200, description="Status of project updated successfully")
@api.response(model=project_not_found_model, code=404, description="No project by that id was found")
@api.param('project_id', 'The project unique identifier')
class UpdateStatusResource(Resource):
    @api.expect(update_status_model)
    @api.doc('update status of project')
    def patch(self, project_id):
        """Update status"""
        data = api.payload
        project = Project.query.filter(Project.id == project_id).first()
        if not project:
            api.logger.info(f"No project by id {project_id}")
            return marshal({'message': "No project by that id was found."}, project_not_found_model), 404
        project.project_status = data["project_status"] 
        DB.session.add(project)
        DB.session.commit()
        return  marshal(project, project_get_model) , 200

