"""
configure pytest
"""
import pytest
from pybugsnag.test.helpers import dbg


@pytest.fixture(scope="session", autouse=True)
def before_all(request):
    """test setup"""
    dbg("[+] begin pybugsnag tests")
    request.addfinalizer(after_all)


def after_all():
    """tear down"""
    dbg("[+] end pybugsnag tests")
