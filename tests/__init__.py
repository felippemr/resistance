import json
import os
import random
import string
import types
from time import sleep
from functools import wraps
import tornado.testing
import pymongo
from app import make_app


def wait_to_start(seconds):
    def decorator(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            sleep(seconds)
            f(*args, **kwargs)
        return wrapped_f
    return decorator


def insert_resources_before_test(n):
    def decorator(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            for _ in range(n):
                args[0].db.resources.insert(
                    {"name": ''.join(
                        random.sample(
                            (string.ascii_uppercase + string.digits), 5
                        )
                    )}
                )
            f(*args, **kwargs)
        return wrapped_f
    return decorator


def get_resource_before_test():
    def decorator(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            resource = args[0].db.resources.find_one()
            args[0].prepare_resource(resource)
            kwargs['resource'] = resource
            f(*args, **kwargs)
        return wrapped_f
    return decorator


class ResourcesApiTestCase(tornado.testing.AsyncHTTPTestCase):
    def setUp(self):
        self.database_name = 'test_resistance'
        self.db = getattr(pymongo.MongoClient(), self.database_name)
        super(ResourcesApiTestCase, self).setUp()
        self._AsyncHTTPTestCase__port = 8888

    def get_app(self):
        os.environ['RESISTANCE_DATABASE_NAME'] = self.database_name
        self.start_real_app()
        sleep(0.3)
        return make_app()

    def start_real_app(self):
        os.system('make run')

    def stop_real_app(self):
        os.system(
            "kill -9 $(ps -ef | grep python | grep -v 'grep' | grep -v 'Anaconda' | grep -v 'unittest' | awk '{print $2}')"
        )

    def drop_mongo_database(self):
        pymongo.MongoClient().drop_database(self.database_name)

    def update_db_variable(self):
        os.environ['RESISTANCE_DATABASE_NAME'] = 'resistance'

    def tearDown(self):
        self.update_db_variable()
        self.stop_real_app()
        self.drop_mongo_database()

    def prepare_resource(self, resouce):
        resouce['_id'] = str(resouce['_id'])

    def get_one_resource(self,):
        resource = self.db.resources.find_one()
        self.prepare_resource(resource)
        return resource

    def find_one_later(self):
        resource = self.db.resources.find_one()
        yield {"_id": str(resource["_id"])}

    def assert_response(self, response, code, body, reason):
        if isinstance(body, types.GeneratorType):
            body = next(body)

        if response.body:
            decoded_body = json.loads(response.body.decode("utf-8"))
            self.assertEqual(decoded_body, body)
        else:
            self.assertEqual(response.body, body)

        self.assertEqual(response.code, code)
        self.assertEqual(response.reason, reason)
