"""The tests to run in this project.
To run the tests type,
$ nosetests --verbose
"""

from nose.tools import assert_true
import requests

BASE_URL = "http://localhost:5000"


def test_get_individual_request_404():
    "Test getting a non existent request"
    response = requests.get('%s/request/an_incorrect_id' % (BASE_URL))
    assert_true(response.status_code == 404)
