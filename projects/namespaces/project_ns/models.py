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


new_stage_model = Model(
       "Stages of the project",
    {
        "name" : fields.String(required=True, description="Name of the stage"),
        "budget" : fields.Integer(required=True, description="Budget needed for this stage"),
        "number" : fields.Integer(required=True, description="Ordinal number of the stage")
    },
)

location_model = Model(
    "Location of project Model",
    {
        "country" : fields.String(required=False, description="Country of project"),
        "latitude": fields.Float(required=False, description="Latitude of project"),
        "longitude": fields.Float(required=False, description="Longitude of project")
    }
)

user_new_project_model = Model(
    "User new project model",
    {
    "title": fields.String(required=True, description="Project title."),
     "description": fields.String(required=True, description="Project Description"),
     "hashtags": fields.List(fields.String,required=False, description="List of hashtags related to project."),
     "project_type": fields.String(required=False, description="Type of project"), #TODO: revisar que tipos
     "images" : fields.List(fields.String,required=False, description="List of images URLs"),
     "videos" : fields.List(fields.String,required=False, description="List of videos URLs"),
     "end_date" : fields.Date(required=False, description="Date when project ends"),
     "location" : fields.Nested(location_model, required=False),
     "user_id" : fields.String(required=True, description="Owner of project"),
     "target_amount" : fields.Integer(required=True, description="Money needed for the project"),
     "creation_date" : fields.Date(required=False, description="Creation date"),
     "status" : fields.String(required=False, enum=["initialized", "pending", "in_progres", "ended"], description="Project status"),
     "stages" : fields.List(fields.Nested(new_stage_model), required=True),
    }
)

new_project_model = Model.inherit(
    "Project model", user_new_project_model,
    {
        "overseers": fields.List(fields.String, required=True, description="List Ids for oveseers"),
        "wallet_id" : fields.String(required=True, description="Wallet id associated to project")
    }
)

project_put_model = Model.inherit('Project put Dto', new_project_model, {
    "id": fields.Integer(readonly=True, description="Id for this type")
} )

project_get_model = Model.inherit('Project get Dto', new_project_model, {
    "id": fields.Integer(readonly=True, description="Id for this type"),
    "overseers" : fields.List(fields.String),
    "sponsors" : fields.List(fields.String)

} )


project_get_pagination_model = Model(
    "Get projects with pagination model", {
     "has_next" : fields.Boolean(),
     "projects" : fields.List(fields.Nested(project_get_model))
    }
)

project_not_found_model = Model(
    "Error message for not found",
    {
     "message" : fields.String(required=True, description="Error message for project not found")
    }
)

