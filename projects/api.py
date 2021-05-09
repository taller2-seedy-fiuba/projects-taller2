"""API module."""
import logging

from flask_restx import Api

from projects import __version__

from projects.namespaces import default_namespace

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


api = Api(prefix="", version=__version__, validate=True)
api.add_namespace(default_namespace, path='/projects')


@api.errorhandler
def handle_exception(error: Exception):
    """When an unhandled exception is raised"""
    message = "Error: " + getattr(error, 'message', str(error))
    return {'message': message}, getattr(error, 'code', 500)
