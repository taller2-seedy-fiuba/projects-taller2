"""Default namespace models module."""

from flask_restx import Model, fields
from projects.namespaces.overseer_ns.models import overseer_assigned_model
from projects.namespaces.sponsor_ns.models import sponsor_model


image_model = Model(
       "Project Image",
    {
        "url": fields.String(required=True, description="URL location for the image"),
        "id": fields.String(readonly=True, description="UUID for this image"),
    },
)
video_model = Model(
       "Project Video",
    {
        "url": fields.String(required=True, description="URL location for the video"),
        "id": fields.String(readonly=True, description="UUID for this video"),
    },
)
hashtag_model = Model(
       "Hashtags for project",
    {
        "name": fields.String(required=True, description="URL location for the image"),
        "id": fields.Integer(readonly=True, description="Id for this hashtag"),
    },
)
new_project_model = Model(
    "Project model",
    {
    "title": fields.String(required=True, description="Project title."),
     "description": fields.String(required=True, description="Project Description"),
     "hashtags": fields.List(fields.Nested(hashtag_model), description="List of hashtags related to project."),
     "project_type": fields.String(required=False, description="Type of project"), #TODO: revisar que tipos
     "images" : fields.List(fields.String,required=False, description="List of images URLs"),
     "videos" : fields.List(fields.String,required=False, description="List of videos URLs"),
     "end_date" : fields.Date(required=False, description="Date when project ends"),
     "location" : fields.String(required=False, description="Project location."),
     "user_id" : fields.String(required=True, description="Owner of project"),
     "target_amount" : fields.Integer(required=True, description="Money needed for the project"),
     "creation_date" : fields.Date(required=False, description="Creation date"),
     "status" : fields.String(required=False, description="Project status"),
    }
)

project_get_model = Model.inherit('Project get Dto', new_project_model, {
    "id": fields.Integer(readonly=True, description="Id for this type"),
    "overseers" : fields.List(fields.Nested(overseer_assigned_model)),
    "sponsors" : fields.List(fields.Nested(sponsor_model))

} )


project_get_pagination_model = Model.inherit(
    "Get projects with pagination model", project_get_model, {
     "has_next" : fields.Boolean()
    }
)

project_not_found_model = Model(
    "Error message for not found",
    {
     "message" : fields.String(required=True, description="Error message for project not found")
    }
)

