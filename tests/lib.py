# pylint: disable=missing-docstring,redefined-outer-name
from types import ModuleType as Module
from unittest import mock

from unittest_fixtures import FixtureContext, Fixtures, fixture

from gbp_webhook_tts import utils

FC = FixtureContext
Mock = mock.Mock


@fixture()
def boto3_session(_: Fixtures, target: Module = utils.boto3) -> FC[Mock]:
    with mock.patch.object(target, "Session") as mock_obj:
        yield mock_obj
