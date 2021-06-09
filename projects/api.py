"""API module."""
import logging

from flask_restx import Api

from projects import __version__

from projects.namespaces.project_ns.projects import api as project_namespace
from projects.namespaces.users_ns.users import api as users_namespace
from projects.namespaces.overseer_ns.overseer import api as overseer_namespace

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


api = Api(prefix="/v1", version=__version__, validate=True)
api.add_namespace(project_namespace, path='/projects')
api.add_namespace(users_namespace, path='/users')
api.add_namespace(overseer_namespace, path='/overseer')


@api.errorhandler
def handle_exception(error: Exception):
    """When an unhandled exception is raised"""
    message = "Error: " + getattr(error, 'message', str(error))
    return {'message': message}, getattr(error, 'code', 500)