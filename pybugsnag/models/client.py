"""
base client model to create and use http endpoints
"""
import requests
import urllib.parse
from pybugsnag.globals import __version__, API_URL, LIBRARY, TEST_TOKEN, TEST_API_URL
from pybugsnag.models.error import RateLimited
from pybugsnag.models import Organization, User


def test_client():
    """returns a test client"""
    return BugsnagDataClient(TEST_TOKEN, api_url=TEST_API_URL, debug=True)


class BugsnagDataClient:
    """client http wrapper"""

    def __init__(self, token, api_url=API_URL, cache=True, debug=False):
        """creates a new client"""
        if not token:
            raise Exception("no token specified!")
        self.token = token
        self.api_url = api_url
        self.version = __version__
        self.cache = cache
        self.debug = debug

        # cache
        self._organizations = None

    @property
    def headers(self):
        """forms the headers required for the API calls"""
        return {
            "Accept": "application/json; version=2",
            "AcceptEncoding": "gzip, deflate",
            "Authorization": "token {}".format(self.token),
            "User-Agent": "{}/{}".format(LIBRARY, self.version),
        }

    def _log(self, *args):
        """logging method"""
        if not self.debug:
            return
        print(*args)

    def _req(self, path, method="get", **kwargs):
        """requests wrapper"""
        full_path = urllib.parse.urljoin(self.api_url, path)
        self._log("[{}]: {}".format(method.upper(), full_path))
        request = requests.request(method, full_path, headers=self.headers, **kwargs)
        if request.status_code == 429:
            raise RateLimited()
        return request

    def get(self, path, **kwargs):
        """makes a get request to the API"""
        return self._req(path, **kwargs).json()

    def post(self, path, **kwargs):
        """makes a post request to the API"""
        return self._req(path, method="post", **kwargs).json()

    def put(self, path, **kwargs):
        """makes a put request to the API"""
        return self._req(path, method="put", **kwargs).json()

    @property
    def organizations(self):
        """organizations list for this access token"""
        if not self._organizations or not self.cache:
            self._organizations = [
                Organization(x, client=self) for x in self.get("user/organizations")
            ]
        return self._organizations
