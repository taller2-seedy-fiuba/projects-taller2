"""API module."""
import logging

from flask_restx import Api

from projects import __version__

from projects.namespaces.project_ns.projects import api as project_namespace

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


api = Api(prefix="/v1", version=__version__, validate=True)
api.add_namespace(project_namespace, path='/projects')
#api.add_namespace(projecgit stt_namespace, path='/projects/{user_id}')


@api.errorhandler
def handle_exception(error: Exception):
    """When an unhandled exception is raised"""
    message = "Error: " + getattr(error, 'message', str(error))
    return {'message': message}, getattr(error, 'code', 500)