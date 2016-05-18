# coding: utf-8
import asyncio
import motor
import tornado
from bson.objectid import ObjectId
from .json_handler import JsonHandler
from . import http_status


class MetaResourceHandler(JsonHandler):
    def _get_collection(self):
        return self.settings['db'].resources

    def _get_resource(self, resource_id):
        resources = self._get_collection()
        return resources.find_one(
            {"_id": ObjectId(resource_id)}
        )

    def _prepare_resource(self, resource):
        resource['_id'] = str(resource['_id'])
        return resource

    def _exit_exception_500(self, e):
        print(e)
        self.write_json_error(
            status_code=http_status.HTTP_500,
            message="Not able to perform request"
        )


class ResourcesWithParamRESTHandler(MetaResourceHandler):

    async def get(self, resource_id):
        resources = self._get_collection()
        try:
            resource = await self._get_resource(resource_id)
        except Exception as e:
            self._exit_exception_500(e)
        else:
            if resource:
                self.update_response(
                    self._prepare_resource(resource)
                )
            else:
                self.write_json_error(status_code=http_status.HTTP_400)

        self.finish_request()

    async def patch(self, resource_id):
        arguments = self.get_json_arguments(force_presence=True)
        resources = self._get_collection()
        try:
            result = await resources.update(
                {'_id': ObjectId(resource_id)}, {'$set': arguments}
            )
        except Exception as e:
            self._exit_exception_500(e)
        else:
            if result['updatedExisting']:
                self.update_response(
                    self._prepare_resource({"_id": ObjectId(resource_id)})
                )
                self.finish_request()
            else:
                self.write_json_error(status_code=http_status.HTTP_400)

    async def delete(self, resource_id):
        resources = self._get_collection()

        try:
            result = await resources.remove({'_id': ObjectId(resource_id)})
        except Exception as e:
            self._exit_exception_500(e)
        else:
            if result['n'] == 1:
                self.update_response(
                    self._prepare_resource({"_id": ObjectId(resource_id)})
                )
                self.finish_request()
            else:
                self.write_json_error(status_code=http_status.HTTP_400)


class ResourcesWithoutParamRESTHandler(MetaResourceHandler):

    async def post(self):
        arguments = self.get_json_arguments(force_presence=True)
        resources = self._get_collection()

        try:
            resource = await resources.insert({**arguments})
        except Exception as e:
            self._exit_exception_500(e)
        else:
            self.update_response(
                self._prepare_resource({"_id": resource})
            )
            self.finish_request(status_code=http_status.HTTP_201)

    async def get(self):
        resources = self._get_collection()
        self.update_response(info={"resources": list()})
        try:
            async for resource in resources.find():
                self._response['resources'].append(
                    self._prepare_resource(resource)
                )
        except Exception as e:
            self._exit_exception_500(e)
        else:
            if not self._response.get('resources', None):
                self.write_json_error(status_code=http_status.HTTP_400)

            self.finish_request()
