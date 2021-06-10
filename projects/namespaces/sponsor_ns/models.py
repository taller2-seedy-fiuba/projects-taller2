"""Models related to Sponsor."""

from flask_restx import Model, fields


sponsor_assigned_model = Model(
       "Sponsor assigned project",
    {
        "id": fields.String(description="Id of Sponsor"),
        "project_id": fields.String(description="Id of project")
    }
)

sponsor_model = Model(
       "Sponsor assigned project",
    {
        "id": fields.String(description="Id of Sponsor"),
    }
)