import operator as ops

from projects.utils import FilterParam
from flask_restx import reqparse

class ProjectQueryParams:

    def __init__(self):
        self.projects_parser = reqparse.RequestParser()

    def add_arguments(self):

        self.projects_parser.add_argument(
            "project_type",
            type=str,
            help="type of project",
            store_missing=False
        )

        self.projects_parser.add_argument(
            "project_status",
            type=str,
            help="status of project",
            store_missing=False
        )

        self.projects_parser.add_argument(
            "hashtag",
            type=str,
            help="Hashtag of project",
            store_missing=False
        ) 

        self.projects_parser.add_argument(
            "page",
            type=int,
            help="page",
            store_missing=False
        )  
        self.projects_parser.add_argument(
            "page_size",
            type=int,
            help="Size of page",
            store_missing=False
        )  
        self.projects_parser.add_argument(
            "center_x",
            type=float,
            help="center longitude",
            store_missing=False
        )
        self.projects_parser.add_argument(
            "center_y",
            type=float,
            help="center latitude",
            store_missing=False
        )
        self.projects_parser.add_argument(
            "radius",
            type=float,
            help="serch radius",
            store_missing=False
        )