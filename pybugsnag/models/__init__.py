"""
models for each object in the bugsnag data access api
"""
import json
from datetime import datetime
from pybugsnag.globals import LIBRARY
from pybugsnag.utils.text import (
    filter_locals,
    snakeify,
    dict_to_query_params,
    datetime_to_iso8601,
)


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


class Collaborator(BaseModel):
    """bugsnag user (collaborator) object"""

    def __init__(self, data, **kwargs):
        """override"""
        super(Collaborator, self).__init__(data, **kwargs)

    def __repr__(self):
        """repr"""
        return "<{}.Collaborator[{}] '{}'>".format(LIBRARY, self.id, self.email)


class Event(BaseModel):
    """bugsnag event object"""

    class Sort:
        """event sort enum"""

        class Direction:
            """event sort direction enum"""

            ASCENDING = "asc"
            DESCENDING = "desc"

        TIMESTAMP = "timestamp"

    def __init__(self, data, **kwargs):
        """override"""
        super(Event, self).__init__(data, **kwargs)

    def __repr__(self):
        """repr"""
        return "<{}.Event[{}] '{}'>".format(LIBRARY, self.id, self.context)


class Pivot(BaseModel):
    """bugsnag pivot object"""

    def __init__(self, data, **kwargs):
        """override"""
        super(Pivot, self).__init__(data, **kwargs)

    def __repr__(self):
        """repr"""
        return "<{}.Pivot[{}] '{}'>".format(
            LIBRARY, self.event_field_display_id, self.name
        )


class Error(BaseModel):
    """bugsnag error object"""

    MIN_BUCKETS = 1
    MAX_BUCKETS = 50

    class Resolution:
        """time resolution enum"""

        ONE_MINUTE = "1m"
        FIVE_MINUTE = "5m"
        THIRTY_MINUTE = "30m"
        TWO_HOUR = "2h"
        TWELVE_HOUR = "12h"

    class Sort:
        """error sort enum"""

        class Direction:
            """error sort direction enum"""

            ASCENDING = "asc"
            DESCENDING = "desc"

        LAST_SEEN = "last_seen"
        FIRST_SEEN = "first_seen"
        USERS = "users"
        EVENTS = "events"
        UNSORTED = "unsorted"

    class Severity:
        """severity enum"""

        ERROR = "error"
        WARNING = "warning"
        INFO = "info"

    def __init__(self, data, **kwargs):
        """override"""
        super(Error, self).__init__(data, **kwargs)

    def __repr__(self):
        """repr"""
        return "<{}.Error[{}] '{}'>".format(LIBRARY, self.id, self.error_class)

    def get_event(self, event_id):
        """gets an event by id for this error"""
        return Event(
            self._client.get("projects/{}/events/{}".format(self.project.id, event_id)),
            client=self._client,
            project=self.project,
            error=self,
        )

    def get_latest_event(self):
        """gets the latest event for this error"""
        return Event(
            self._client.get("errors/{}/latest_event".format(self.id)),
            client=self._client,
            project=self.project,
            error=self,
        )

    def get_events(
        self,
        base=None,
        sort=Event.Sort.TIMESTAMP,
        direction=Event.Sort.Direction.DESCENDING,
        per_page=30,
        filters=None,  # TODO
        full_reports=False,
        **kwargs
    ):
        """get events for this error"""
        params = filter_locals(locals())

        if "base" not in params:
            params["base"] = datetime.now()

        query_params = dict_to_query_params(params)
        path = "projects/{}/errors/{}/events{}".format(
            self.project.id, self.id, query_params
        )
        return [
            Event(x, error=self, client=self._client, project=self.project)
            for x in self._client.get(path)
        ]

    def get_trend_buckets(self, buckets_count=10):
        """get trend buckets for this error"""
        buckets = min(max(Error.MIN_BUCKETS, buckets_count), Error.MAX_BUCKETS)
        return self._client.get(
            "projects/{}/errors/{}/trend?buckets_count={}".format(
                self.project.id, self.id, buckets
            )
        )

    def get_trend_resolution(self, resolution=None):
        """get trend buckets for this error based on time resolution"""
        if not resolution:
            resolution = Error.Resolution.FIVE_MINUTE
        return self._client.get(
            "projects/{}/errors/{}/trend?resolution={}".format(
                self.project.id, self.id, resolution
            )
        )

    def get_pivots(self, summary_size=10, per_page=30):
        """get a number of pivots for this error"""
        params = filter_locals(locals())
        query_params = dict_to_query_params(params)
        return [
            Pivot(x, project=self.project, error=self, client=self._client)
            for x in self._client.get(
                "projects/{}/errors/{}/pivots{}".format(
                    self.project.id, self.id, query_params
                )
            )
        ]


class Release(BaseModel):
    """bugsnag release object"""

    class Sort:
        """release sort enum"""

        class Direction:
            """release sort direction enum"""

            ASCENDING = "asc"
            DESCENDING = "desc"

        TIMESTAMP = "timestamp"
        PERCENT_OF_SESSIONS = "percent_of_sessions"
        CRASH_RATE = "crash_rate"
        PERCENT_OF_EVENTS = "percent_of_events"

    def __init__(self, data, **kwargs):
        """override"""
        super(Release, self).__init__(data, **kwargs)

    def __repr__(self):
        """repr"""
        return "<{}.Release[{}] '{}'>".format(LIBRARY, self.id, self.app_version)


class Project(BaseModel):
    """bugsnag project object"""

    MIN_BUCKETS = 1
    MAX_BUCKETS = 50

    class Resolution:
        """time resolution enum"""

        ONE_MINUTE = "1m"
        FIVE_MINUTE = "5m"
        THIRTY_MINUTE = "30m"
        TWO_HOUR = "2h"
        TWELVE_HOUR = "12h"

    class Sort:
        """project sort enum"""

        class Direction:
            """project sort direction enum"""

            ASCENDING = "asc"
            DESCENDING = "desc"

        CREATED_AT = "created_at"

    def __init__(self, data, **kwargs):
        """override"""
        super(Project, self).__init__(data, **kwargs)

    def __repr__(self):
        """repr"""
        return "<{}.Project[{}] '{}'>".format(LIBRARY, self.id, self.name)

    def get_error(self, error_id):
        """gets an error by id for this project"""
        return Error(
            self._client.get("projects/{}/errors/{}".format(self.id, error_id)),
            client=self._client,
            project=self,
        )

    def get_errors(
        self,
        base=None,
        sort=Error.Sort.LAST_SEEN,
        direction=Error.Sort.Direction.DESCENDING,
        per_page=30,
        filters=None,  # TODO
        **kwargs
    ):
        """get errors for this project"""
        params = filter_locals(locals())

        if "base" not in params:
            params["base"] = datetime.now()

        query_params = dict_to_query_params(params)
        path = "projects/{}/errors{}".format(self.id, query_params)
        return [
            Error(x, project=self, client=self._client) for x in self._client.get(path)
        ]

    def get_event(self, event_id):
        """gets an event by id for this project"""
        return Event(
            self._client.get("projects/{}/events/{}".format(self.id, event_id)),
            client=self._client,
            project=self,
        )

    def get_events(
        self,
        base=None,
        sort=Event.Sort.TIMESTAMP,
        direction=Event.Sort.Direction.DESCENDING,
        per_page=30,
        filters=None,  # TODO
        full_reports=False,
        **kwargs
    ):
        """get events for this project"""
        params = filter_locals(locals())

        if "base" not in params:
            params["base"] = datetime.now()

        query_params = dict_to_query_params(params)
        path = "projects/{}/events{}".format(self.project.id, query_params)
        return [
            Event(x, project=self, client=self._client) for x in self._client.get(path)
        ]

    def get_trend_buckets(self, buckets_count=10):
        """get trend buckets for this project"""
        buckets = min(max(Project.MIN_BUCKETS, buckets_count), Project.MAX_BUCKETS)
        return self._client.get(
            "projects/{}/trend?buckets_count={}".format(self.id, buckets)
        )

    def get_trend_resolution(self, resolution=None):
        """get trend buckets for this project based on time resolution"""
        if not resolution:
            resolution = Project.Resolution.FIVE_MINUTE
        return self._client.get(
            "projects/{}/trend?resolution={}".format(self.id, resolution)
        )

    def get_release(self, release_id):
        """get a single release by id"""
        return Release(
            self._client.get("projects/{}/releases/{}".format(self.id, release_id)),
            project=self,
            client=self._client,
        )

    def get_releases(
        self,
        release_stage=None,
        base=None,
        sort=Release.Sort.TIMESTAMP,
        offset=0,
        per_page=5,
    ):
        """get a list of releases for this project"""
        params = filter_locals(locals())

        if "base" in params:
            params["base"] = datetime_to_iso8601(params["base"])

        query_params = dict_to_query_params(params)
        path = "projects/{}/releases{}".format(self.id, query_params)
        return [
            Release(x, project=self, client=self._client)
            for x in self._client.get(path)
        ]

    def get_pivots(self, summary_size=10):
        """get a number of pivots for this project"""
        params = filter_locals(locals())
        query_params = dict_to_query_params(params)
        return [
            Pivot(x, project=self, client=self._client)
            for x in self._client.get(
                "projects/{}/pivots{}".format(self.id, query_params)
            )
        ]


class Organization(BaseModel):
    """bugsnag organization object"""

    def __init__(self, data, **kwargs):
        """override"""
        super(Organization, self).__init__(data, **kwargs)
        self._projects = None
        self._collaborators = None
        self._admins_count = None

    def __repr__(self):
        """repr"""
        return "<{}.Organization[{}] '{}'>".format(LIBRARY, self.id, self.name)

    @property
    def projects(self):
        """cachable projects property"""
        if not self._projects or not self._client.cache:
            self._projects = self.get_projects()
        return self._projects

    @property
    def collaborators(self):
        """cachable collaborators property"""
        if not self._collaborators or not self._client.cache:
            self._collaborators = self.get_collaborators()
        return self._collaborators

    @property
    def admins_count(self):
        """gets the count of admin collaborators"""
        if not self._admins_count or not self._client.cache:
            self._admins_count = int(
                self._client.get(
                    "organizations/{}/admins_count".format(self.id), raw=True
                ).text
            )
        return self._admins_count

    def get_projects(
        self,
        sort=Project.Sort.CREATED_AT,
        direction=Project.Sort.Direction.DESCENDING,
        per_page=30,
    ):
        """gets the projects based on the params"""
        params = filter_locals(locals())
        query_params = dict_to_query_params(params)

        path = "organizations/{}/projects{}".format(self.id, query_params)
        return [
            Project(x, organization=self, client=self._client)
            for x in self._client.get(path)
        ]

    def get_collaborators(self, per_page=30, q=None, exclude_project=None):
        """get collaborators for this organization"""
        params = filter_locals(locals())
        query_params = dict_to_query_params(params)

        path = "organizations/{}/collaborators{}".format(self.id, query_params)
        return [
            Collaborator(x, organization=self, client=self._client)
            for x in self._client.get(path)
        ]

    def get_collaborator(self, collaborator_id):
        """get collaborator by id"""
        return Collaborator(
            self._client.get(
                "organizations/{}/collaborators/{}".format(self.id, collaborator_id)
            ),
            organization=self,
            client=self._client,
        )
