from . import (
    wait_to_start, insert_resources_before_test, ResourcesApiTestCase,
    get_resource_before_test)


class ResourcesApiTest(ResourcesApiTestCase):
    @insert_resources_before_test(2)
    def test_get_many_resources_ok(self):
        resources = {'resources': []}
        for resource in self.db.resources.find():
            self.prepare_resource(resource)
            resources['resources'].append(resource)

        self.assert_response(
            self.fetch('/api/v0.1/resources', method='GET'),
            200, resources, 'OK'
        )

    def test_get_all_resources_fail(self):
        self.assert_response(
            self.fetch('/api/v0.1/resources', method='GET'),
            400, b'', 'Bad Request'
        )

    @insert_resources_before_test(n=1)
    @get_resource_before_test()
    def test_get_single_resource_ok(self, resource):
        self.assert_response(
            self.fetch(
                '/api/v0.1/resources/{}'.format(resource['_id']),
                method='GET'
            ),
            200, resource, 'OK'
        )

    def test_get_single_resource_fails(self):
        self.assert_response(
            self.fetch(
                '/api/v0.1/resources/bed896005177cc528ddd4375', method='GET'
            ),
            400, b'', 'Bad Request'
        )

    def test_create_resource_ok(self):
        self.assert_response(
            self.fetch(
                '/api/v0.1/resources', method='POST', body='{"name":"test"}'
            ),
            201, self.find_one_later(), 'Created'
        )

    def test_create_resource_fails(self):
        self.assert_response(
            self.fetch(
                '/api/v0.1/resources', method='POST', body=''
            ),
            400, {'message': 'JSON is required for this method'}, 'Bad Request'
        )

    @insert_resources_before_test(n=1)
    @get_resource_before_test()
    def test_delete_resource_ok(self, resource):
        self.assert_response(
            self.fetch(
                '/api/v0.1/resources/{}'.format(resource['_id']),
                method='DELETE',
            ), 200, {"_id": resource['_id']}, 'OK'
        )

    def test_delete_resource_fails(self):
        self.assert_response(
            self.fetch(
                '/api/v0.1/resources/bed896005177cc528ddd4375',
                method='DELETE',
            ), 400, b'', 'Bad Request'
        )

    @insert_resources_before_test(n=1)
    @get_resource_before_test()
    def test_update_resource_ok(self, resource):
        self.assert_response(
            self.fetch(
                '/api/v0.1/resources/{}'.format(resource['_id']),
                method='PATCH', body='{"type":"test"}'
            ), 200, {"_id": resource['_id']}, 'OK'
        )

        resource["type"] = "test"
        _resource = self.get_one_resource()
        self.assertEqual(resource, _resource)

    @wait_to_start(0.5)
    @insert_resources_before_test(n=1)
    @get_resource_before_test()
    def test_update_resource_fails(self, resource):
        self.assert_response(
            self.fetch(
                '/api/v0.1/resources/{}'.format(resource['_id']),
                method='PATCH', body=''
            ), 400, {"message": "JSON is required for this method"},
            'Bad Request'
        )

        self.assert_response(
            self.fetch(
                '/api/v0.1/resources/bed896005177cc528ddd4375',
                method='PATCH', body='{"type":"2"}'
            ), 400, b'', 'Bad Request'
        )
