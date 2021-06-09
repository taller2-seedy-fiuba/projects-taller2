"""Models related to Overseer."""

from flask_restx import Model, fields

assign_overseer_model = Model(
       "Assign overseer to project",
    {
        "user_id": fields.String(required=True, description="Id of Overseer"),
        "project_id": fields.Integer(required=True, description="Id of project to assign overseer"),
    }
)

overseer_assigned_model = Model(
       "overseer assigned project",
    {
        "id": fields.String(description="Id of Overseer"),
        "confirmed": fields.Boolean(description="Overseer confirmed the assign"),
    }
)