import requests
import json
from flask import request



class Client:
    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get(self, endpoint, params):
        if bool(params):
            response = requests.get(self.baseurl + endpoint, params)
        else:
            response = requests.get(self.baseurl + endpoint)
        return response.json(), response.status_code

    def get_by_id(self, endpoint, project_id):
        response = requests.get(self.baseurl + endpoint + "/" + str(project_id))
        return response.json(), response.status_code

    def post(self, endpoint, payload):
        response = requests.post(self.baseurl + endpoint, data=payload)
        return response.json(), response.status_code