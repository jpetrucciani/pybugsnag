"""
a base test suite for pybugsnag
"""
from datetime import datetime
from pybugsnag.models import (
    Collaborator,
    Error,
    Event,
    EventField,
    Organization,
    Pivot,
    Project,
    Release,
)
from pybugsnag.models.client import test_client


CLIENT = test_client()


def is_list_of_type(check_list, check_type):
    """helper function for checking if it's a list and of a specific type"""
    assert isinstance(check_list, list)
    assert isinstance(check_list[0], check_type)
    return True


def test_organizations():
    """testing accessing organizations"""
    organizations = CLIENT.organizations
    assert organizations
    assert isinstance(organizations, list)

    organization = organizations[0]
    assert organization
    assert isinstance(organization, Organization)

    found_organization = CLIENT.get_organization(organization.id)
    assert isinstance(found_organization, Organization)

    assert isinstance(organization.created_at, datetime)
    assert isinstance(organization.updated_at, datetime)

    assert organization.admins_count == 5
    assert is_list_of_type(organization.collaborators, Collaborator)
    assert is_list_of_type(organization.projects, Project)

    found_collaborator = organization.get_collaborator(organization.collaborators[0].id)
    assert isinstance(found_collaborator, Collaborator)

    assert "<pybugsnag.Collaborator" in str(found_collaborator)
    assert "<pybugsnag.Organization" in str(organization)


def test_projects():
    """testing features around projects"""
    organization = CLIENT.organizations[0]
    assert organization
    assert is_list_of_type(organization.projects, Project)
    project = organization.projects[0]

    found_project = CLIENT.get_project(project.id)
    assert isinstance(found_project, Project)

    assert isinstance(project.created_at, datetime)
    assert isinstance(project.updated_at, datetime)

    errors = project.get_errors()
    assert is_list_of_type(errors, Error)

    error_found = project.get_error(errors[0].id)
    assert isinstance(error_found, Error)

    events = project.get_events()
    assert is_list_of_type(events, Event)

    event_found = project.get_event(events[0].id)
    assert isinstance(event_found, Event)

    releases = project.get_releases()
    assert is_list_of_type(releases, Release)

    # TODO reimplement when the apiary is fixed
    # release_found = project.get_release(releases[0].id)
    # assert isinstance(release_found, Release)

    trend_buckets = project.get_trend_buckets()
    assert is_list_of_type(trend_buckets, dict)

    trend_resolution = project.get_trend_resolution()
    assert is_list_of_type(trend_resolution, dict)

    pivots = project.get_pivots()
    assert is_list_of_type(pivots, Pivot)

    event_fields = project.get_event_fields()
    assert is_list_of_type(event_fields, EventField)

    assert "<pybugsnag.Release" in str(releases[0])
    assert "<pybugsnag.EventField" in str(event_fields[0])


def test_errors():
    """testing features around errors"""
    organization = CLIENT.organizations[0]
    assert organization
    assert isinstance(organization.projects, list)

    project = organization.projects[0]
    assert isinstance(project, Project)

    errors = project.get_errors()
    assert is_list_of_type(errors, Error)

    error = errors[0]
    events = error.get_events()
    assert is_list_of_type(events, Event)
    assert isinstance(events[0].project, Project)
    assert isinstance(error.first_seen, datetime)
    assert isinstance(error.last_seen, datetime)
    assert isinstance(error.first_seen_unfiltered, datetime)

    latest_event = error.get_latest_event()
    assert isinstance(latest_event, Event)

    found_event = error.get_event(latest_event.id)
    assert isinstance(found_event, Event)

    trend_buckets = error.get_trend_buckets()
    assert is_list_of_type(trend_buckets, dict)

    trend_resolution = error.get_trend_resolution()
    assert is_list_of_type(trend_resolution, dict)

    pivots = error.get_pivots()
    assert is_list_of_type(pivots, Pivot)

    assert "<pybugsnag.Error" in str(error)
    assert "<pybugsnag.Pivot" in str(pivots[0])


def test_events():
    """testing features around events"""
    organization = CLIENT.organizations[0]
    assert organization
    assert isinstance(organization.projects, list)

    project = organization.projects[0]
    assert isinstance(project, Project)

    errors = project.get_errors()
    assert is_list_of_type(errors, Error)
    error = errors[0]

    events = error.get_events()
    assert is_list_of_type(events, Event)
    event = events[0]

    assert isinstance(event.received_at, datetime)
    assert "<pybugsnag.Event" in str(event)
