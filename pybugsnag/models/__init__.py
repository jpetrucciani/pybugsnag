"""
models for each object in the bugsnag data access api
"""
import json
from pybugsnag.globals import LIBRARY
from pybugsnag.utils.text import filter_locals, snakeify


class BaseModel:
    """basic model that just parses camelCase json to snake_case keys"""

    def __init__(self, data, client=None, **kwargs):
        """constructor"""
        self._data = {**data, **kwargs}
        self._json = self._jsond(data)
        self._client = client

        for key in self._data:
            setattr(self, snakeify(key), self._data[key])

    def _jsond(self, json_data):
        """json dumps"""
        return json.dumps(json_data)

    def _jsonl(self, dictionary):
        """json loads"""
        return json.loads(dictionary)


class User(BaseModel):
    """user object"""

    def __init__(self, data, **kwargs):
        """override"""
        super(User, self).__init__(data, **kwargs)

    def __repr__(self):
        """repr"""
        return "<{}.User[{}] '{}'>".format(LIBRARY, self.id, self.email)


class Organization(BaseModel):
    """Organization object"""

    def __init__(self, data, **kwargs):
        """override"""
        super(Organization, self).__init__(data, **kwargs)
        self.creator = User(self.creator)
        self._projects = None

    def __repr__(self):
        """repr"""
        return "<{}.Organization[{}] '{}'>".format(LIBRARY, self.id, self.name)

    @property
    def projects(self):
        """cachable projects property"""
        if not self._projects or not self._client.cache:
            self._projects = self.get_projects()
        return self._projects

    def get_projects(self, sort="created_at", direction="desc", per_page=30):
        """gets the projects based on the params"""
        path = "organizations/{}/projects?sort={}&direction={}&per_page={}".format(
            self.id, sort, direction, per_page
        )
        return [Project(x) for x in self._client.get(path)]


class Project(BaseModel):
    """Project object"""

    def __init__(self, data, **kwargs):
        """override"""
        super(Project, self).__init__(data, **kwargs)

    def __repr__(self):
        """repr"""
        return "<{}.Project[{}] '{}'>".format(LIBRARY, self.id, self.name)

    def get_errors(
        self,
        base=None,
        sort=None,
        direction=None,
        per_page=None,
        filters=None,
        **kwargs
    ):
        """get errors for this project"""
        params = filter_locals(locals())

        print(params)

        path = "projects/{}/errors?"


class Error(BaseModel):
    """Error object"""

    def __init__(self, data, **kwargs):
        """override"""
        super(Error, self).__init__(data, **kwargs)

    def __repr__(self):
        """repr"""
        return "<{}.Error[{}] '{}'>".format(LIBRARY, self.id, self.error_class)
