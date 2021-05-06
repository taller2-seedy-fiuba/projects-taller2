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
    {"title": fields.String(required=True, description="Project title."),
     "description": fields.String(required=True, description="Project Description"),
     "hashtags": fields.List(fields.Nested(hashtag_model), description="List of hashtags related to project."),
     "types": fields.List(fields.Nested(type_model),required=False, description="Type of project"), #TODO: revisar que tipos
     "images" : fields.List(fields.Nested(image_model),required=False, description="List of images URLs"),
     "end_date" : fields.DateTime(required=False, description="Date when project ends"),
     "location" : fields.String(required=False, description="Project location.")
    }
)

