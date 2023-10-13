import pytest

def pytest_addoption(parser):
    parser.addoption(
        '--base-url',
        action='store',
        default='https://localhost:4566',
        help='API Gateway Base URL format: https://{api-id}.execute-api.{region}.amazonaws.com/{stage}'
    )

@pytest.fixture
def getBaseUrl(request):
    request.cls.base_url = request.config.getoption('--base-url')

    # params = {}
    # params['base_url'] = request.config.getoption("--base-url")
    # return params