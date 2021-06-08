"""Models related to Overseer."""

from flask_restx import Model, fields

overseer_assigned_model = Model(
       "Assign overseer to project",
    {
        "user_id": fields.String(required=True, description="Id of Overseer"),
        "project_id": fields.Integer(required=True, description="Id of project to assign overseer"),
    }
)