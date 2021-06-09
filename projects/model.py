"""Models for database used in projects."""
from uuid import uuid4
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import UUIDType


DB = SQLAlchemy()

association_table = DB.Table('project_overseer_association', DB.Model.metadata,
    DB.Column('project_id', DB.Integer, DB.ForeignKey('project.id')),
    DB.Column('overseer_id', DB.String, DB.ForeignKey('overseer.id'))
)

class Project(DB.Model):
    __tablename__ = 'project'

    """Projects models."""
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String)
    description = DB.Column(DB.String)
    hashtags = DB.relationship("Hashtag", backref="project", lazy=True)
    project_type = DB.Column(DB.String)
    images = DB.relationship("Image", backref="project", lazy=True)
    videos = DB.relationship("Video", backref="project", lazy=True)
    overseers = DB.relationship(
        "Overseer",
        secondary=association_table,
        back_populates="projects")
    end_date = DB.Column(DB.DateTime)
    location = DB.Column(DB.String) #revisar formato
    user_id = DB.Column(DB.String)
    target_amount = DB.Column(DB.BigInteger)
    status = DB.Column(DB.String)
    creation_date = DB.Column(DB.DateTime)
    #TODO: Revisar otros.

    def update_from_dict(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)


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

class Video(DB.Model):
    """Images for projects."""

    id = DB.Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    url = DB.Column(DB.String, nullable=False)
    project_id = DB.Column(DB.Integer, DB.ForeignKey("project.id"), nullable=False)

class AssignedStatus(Enum):
    pending,
    confirmed,
    rejected

class Overseer(DB.Model):
    __tablename__ = 'overseer'

    """Overseers asigned to projects."""
    id = DB.Column(DB.String, primary_key=True)
    projects = DB.relationship(
        "Project",
        secondary=association_table,
        back_populates="overseers")
    confirmed = DB.Column(DB.Boolean, default=False)
    assigned_status = DB.Column(DB.Enum(AssignedStatus))
