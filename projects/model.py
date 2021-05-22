"""Models for database used in projects."""
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import UUIDType


DB = SQLAlchemy()


class Project(DB.Model):
    """Projects models."""
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String)
    description = DB.Column(DB.String)
    hashtags = DB.relationship("Hashtag", backref="project", lazy=True)
    project_type = DB.Column(DB.String)
    images = DB.relationship("Image", backref="project", lazy=True)
    end_date = DB.Column(DB.DateTime)
    location = DB.Column(DB.String) #revisar formato
    user_id = DB.Column(DB.String)
    target_amount = DB.Column(DB.BigInteger)
    status = DB.Column(DB.String)
    creation_date = DB.Column(DB.DateTime)
    #TODO: Revisar otros.


class Hashtag(DB.Model):
    """Hashtags related with the project"""

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String)
    project_id = DB.Column(DB.Integer, DB.ForeignKey('project.id'))


class Image(DB.Model):
    """Images for projects."""

    id = DB.Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    url = DB.Column(DB.String, nullable=False)
    project_id = DB.Column(DB.Integer, DB.ForeignKey("project.id"), nullable=False)
