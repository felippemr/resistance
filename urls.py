# coding: utf-8
from handlers import (
    ResourcesWithoutParamRESTHandler, ResourcesWithParamRESTHandler
)

VERSION = 'v0.1'
PREFIX = '/api/{}'.format(VERSION)


def build_route(route):
    return r'{}{}'.format(PREFIX, route)


URLS = [
    (build_route('/resources'), ResourcesWithoutParamRESTHandler),
    (build_route('/resources/([a-f\d]{24})'), ResourcesWithParamRESTHandler)
]
