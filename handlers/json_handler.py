# coding: utf-8
import json
import tornado.web
from tornado.web import Finish
from . import http_status


class JsonHandler(tornado.web.RequestHandler):
    """Request handler where requests and responses speak JSON."""

    def prepare(self):
        self._response = dict()
        if self.request.body:
            try:
                json_data = tornado.escape.json_decode(self.request.body)
            except(ValueError, json.decoder.JSONDecodeError):
                self.write_json_error(
                    status_code=http_status.HTTP_400,
                    message="Could not parse JSON"
                )
            else:
                self.request.arguments = json_data

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def get_json_arguments(self, force_presence=False):
        arguments = self.request.arguments

        if force_presence and not arguments:
            self.write_json_error(
                status_code=http_status.HTTP_400,
                message="JSON is required for this method"
            )

        return arguments

    def finish_request(self, status_code=http_status.HTTP_200,):
        self.set_status(status_code)
        self.write_json()
        self.finish()

    def write_json_error(self, status_code, message=None):
        if message:
            self.update_response(info={"message": message})
            self.write_json()

        self.set_status(status_code=status_code)
        raise Finish()

    def write_json(self):
        output = json.dumps(self._response)
        self.write(output)

    def update_response(self, info):
        self._response.update(info)
