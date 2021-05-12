"""Default namespace models module."""

from flask_restx import Model, fields

image_model = Model(
       "Project Image",
    {
        "url": fields.String(required=True, description="URL location for the image"),
        "id": fields.String(readonly=True, description="UUID for this image"),
    },
)

hashtag_model = Model(
       "Hashtags for project",
    {
        "name": fields.String(required=True, description="URL location for the image"),
        "id": fields.Integer(readonly=True, description="Id for this hashtag"),
    },
)

type_model = Model(
       "Types for project",
    {
        "name": fields.String(required=True, description="Type for project"), #TODO: Add types
        "id": fields.Integer(readonly=True, description="Id for this type"),
    },
)

new_project_model = Model(
    "Project model",
    {
    "id": fields.Integer(readonly=True, description="Id for this type"),
    "title": fields.String(required=True, description="Project title."),
     "description": fields.String(required=True, description="Project Description"),
     "hashtags": fields.List(fields.Nested(hashtag_model), description="List of hashtags related to project."),
     "project_type": fields.String(required=False, description="Type of project"), #TODO: revisar que tipos
     "images" : fields.List(fields.Nested(image_model),required=False, description="List of images URLs"),
     "end_date" : fields.Date(required=False, description="Date when project ends"),
     "location" : fields.String(required=False, description="Project location."),
     "user_id" : fields.String(required=True, description="Owner of project"),
     "target_amount" : fields.Integer(required=True, description="Money needed for the project"),
     "state" : fields.String(required=False, description="State of project"),
     "creation_date" : fields.Date(required=False, description="Creation date")
    }
)

