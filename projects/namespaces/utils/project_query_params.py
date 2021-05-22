import operator as ops

from projects.utils import FilterParam
from flask_restx import reqparse

class ProjectQueryParams:

    def __init__(self):
        self.projects_parser = reqparse.RequestParser()

    def add_arguments(self):
        self.projects_parser.add_argument(
            "id",
            type=FilterParam("id", ops.eq, schema="int"),
            help="id of project",
            store_missing=False
        )

        self.projects_parser.add_argument(
            "title",
            type=FilterParam("title", ops.eq, schema=str),
            help="title of project",
            store_missing=False
        )

        self.projects_parser.add_argument(
            "description",
            type=FilterParam("description", ops.eq, schema=str),
            help="description of project",
            store_missing=False
        )

        self.projects_parser.add_argument(
            "project_type",
            type=FilterParam("project_type", ops.eq, schema=str),
            help="type of project",
            store_missing=False
        )

        self.projects_parser.add_argument(
            "end_date",
            type=FilterParam("end_date", ops.eq, schema="date"),
            help="deadline of project",
            store_missing=False
        )
        self.projects_parser.add_argument(
            "user_id",
            type=FilterParam("user_id", ops.eq, schema=str),
            help="owner of project",
            store_missing=False
        )
        self.projects_parser.add_argument(
            "status",
            type=FilterParam("status", ops.eq, schema=str),
            help="status of project",
            store_missing=False
        )
        self.projects_parser.add_argument(
            "creation_date",
            type=FilterParam("creation_date", ops.eq, schema="date"),
            help="creation date of project",
            store_missing=False
        )
        self.projects_parser.add_argument(
            "creation_date",
            type=FilterParam("creation_date", ops.eq, schema="date"),
            help="creation date of project",
            store_missing=False
        )            

