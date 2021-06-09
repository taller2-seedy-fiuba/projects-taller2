"""Models related to Overseer."""

from flask_restx import Model, fields

assign_overseer_model = Model(
       "Assign overseer to project",
    {
        "confirmed": fields.Boolean(required=True, description="Overseer accept (True) or reject (False) the project"),
    }
)

overseer_assigned_model = Model(
       "overseer assigned project",
    {
        "id": fields.String(description="Id of Overseer"),
        "id_project": fields.String(description="Id of project")
        "confirmed": fields.Boolean(description="Overseer accept or reject the assign"),
    }
)