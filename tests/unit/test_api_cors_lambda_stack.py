import aws_cdk as core
import aws_cdk.assertions as assertions
import urllib3
import boto3
import json
import pytest



@pytest.mark.usefixtures('getBaseUrl')
class TestDemoAPI(object):
    def setup_class(self):
        pass

    def test_base_url(self):
        print(self.base_url)

    def test_apigw(self):###create assertions
        pass


    # @pytest.mark.skip
    def test_apigw_endpoint(self):
        http = urllib3.PoolManager()

        headers = {}

        num_endpoints_passed = 0
        endpoint = '/example'
        api_endpoint = self.base_url + endpoint
        response = http.request("GET", api_endpoint, None)
        print(f'==> tested: {api_endpoint} ... status: {response.status}')
        json_data = json.loads(response.data)
        print(json_data)

        try:
            assert response.status == 200, f"Expected status code: 200, Actual status code: {response.status}"
            num_endpoints_passed += 1
        except AssertionError as e:
            print(f'AssertionError: {e}')
        #
        # print(f"Number of endpoints passed: {num_endpoints_passed}/{len(paths)}")
        # assert num_endpoints_passed == len(paths), "Not all endpoints passed"

        assert response.status == 200
        # assert response.json() == {'key': 'value'}
