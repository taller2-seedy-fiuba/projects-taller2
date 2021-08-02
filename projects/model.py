"""Models for database used in projects."""
from uuid import uuid4
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import UUIDType
from geoalchemy2 import Geography



DB = SQLAlchemy(session_options={"autoflush": False})

project_overseer_association_table = DB.Table('project_overseer_association', DB.Model.metadata,
    DB.Column('project_id', DB.Integer, DB.ForeignKey('project.id')),
    DB.Column('overseer_id', DB.String, DB.ForeignKey('overseer.id'))
)

project_sponsor_association_table = DB.Table('project_sponsor_association', DB.Model.metadata,
    DB.Column('project_id', DB.Integer, DB.ForeignKey('project.id')),
    DB.Column('sponsor_id', DB.String, DB.ForeignKey('sponsor.id'))
)

class ProjectStatus(Enum):
    initialized = 1,
    in_progres = 2,
    ended = 3,
    pending = 4

class ProjectStatus2(Enum):
    CREATED = 1,
    FUNDING = 2,
    IN_PROGRESS = 3,
    COMPLETED = 4,
    CANCELED = 5,
    NOT_CREATED = 6,
    PENDING = 7

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
        secondary=project_overseer_association_table,
        back_populates="projects")
    sponsors = DB.relationship(
        "Sponsor",
        secondary=project_sponsor_association_table,
        back_populates="projects")
    end_date = DB.Column(DB.DateTime)
    location = DB.relationship('Location', backref='project', lazy=True)
    user_id = DB.Column(DB.String)
    target_amount = DB.Column(DB.BigInteger)
    status = DB.Column(DB.Enum(ProjectStatus), default=ProjectStatus.initialized.value)
    project_status = DB.Column(DB.Enum(ProjectStatus2), default=ProjectStatus2.CREATED.value)

    creation_date = DB.Column(DB.DateTime)
    stages = DB.relationship("Stage", backref="project", lazy=True)
    wallet_id = DB.Column(DB.String)
    #TODO: Revisar otros.

    def update_from_dict(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)

class Location(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    country = DB.Column(DB.String)
    lat = DB.Column(DB.Float)
    lon = DB.Column(DB.Float)
    point = DB.Column(Geography(geometry_type='POINT', srid=4326))
    project_id = DB.Column(DB.Integer, DB.ForeignKey('project.id'))
    

class Stage(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String)
    status = DB.Column(DB.Enum(ProjectStatus, name="stage_status"), default=ProjectStatus.pending)
    budget = DB.Column(DB.BigInteger)
    project_id = DB.Column(DB.Integer, DB.ForeignKey('project.id'))
    number = DB.Column(DB.Integer)

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
    pending = 1,
    confirmed = 2,
    rejected = 3

class Overseer(DB.Model):
    __tablename__ = 'overseer'

    """Overseers asigned to projects."""
    id = DB.Column(DB.String, primary_key=True)
    projects = DB.relationship(
        "Project",
        secondary=project_overseer_association_table,
        back_populates="overseers")
    confirmed = DB.Column(DB.Boolean, default=False)
    assigned_status = DB.Column(DB.Enum(AssignedStatus, name="assigned_status"), default=AssignedStatus.pending)

class Sponsor(DB.Model):
    "Sponsor assigned to projects"
    id = DB.Column(DB.String, primary_key=True)
    projects = DB.relationship(
        "Project",
        secondary=project_sponsor_association_table,
        back_populates="sponsors")
    favorites = DB.relationship("Favorite", backref="Sponsor", lazy=True)

class Favorite(DB.Model):
    """Favorite projects for sponsors """
    id = DB.Column(DB.Integer, primary_key=True)
    sponsor_id = DB.Column(DB.String, DB.ForeignKey('sponsor.id'))
    project_id = DB.Column(DB.Integer)

