"""Overseer namespace."""

from flask_restx import Namespace, Resource

from flask_restx import Model, fields, marshal
from projects.namespaces.overseer_ns.model import assign_overseer_model, overseer_assigned_model
from projects.model import Project, Overseer, DB
from projects.exceptions import ProjectNotFound

api = Namespace("Overseer", description="Get projects assigned to Overseer.")

api.models[overseer_assigned_model.name] = overseer_assigned_model
api.models[assign_overseer_model.name] = assign_overseer_model


@api.route('/<user_id>/projects')
@api.param('user_id', 'The id of Overseer to be assigned')
class OverseerResource(Resource):
    
    @api.doc('Assign Overseer to Project ')
    @api.expect(assign_overseer_model)
    def put(self, user_id):
        """Assign Overseer to project"""
        data = api.payload
        project = Project.query.filter(Project.id == data['project_id']).first()
        if project is None:
            raise ProjectNotFound
        overseer = Overseer.query.filter(Overseer.id == data['user_id']).first()
        if overseer is None:
            overseer = Overseer(id=data['user_id'])
        overseer.projects.append(project)
        DB.session.add(overseer)
        DB.session.commit()

        return marshal(overseer, overseer_assigned_model)

@api.errorhandler(ProjectNotFound)
def handle_ProjectNotFound(_exception):
    """Handle project not found exception."""
    return {'message': "No project by that id was found."}, 404



