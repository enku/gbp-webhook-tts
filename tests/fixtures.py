# pylint: disable=missing-docstring,redefined-outer-name
import os
import tempfile
from collections.abc import Mapping, MutableMapping
from pathlib import Path
from types import ModuleType
from unittest import mock

from unittest_fixtures import FixtureContext, Fixtures, fixture

from gbp_webhook_tts import handlers, utils


@fixture()
def environ(
    _fixtures: Fixtures, *, environ: Mapping[str, str] | None = None
) -> FixtureContext[MutableMapping[str, str]]:
    environ = environ or {}

    with mock.patch.dict(os.environ, clear=True):
        os.environ.update(environ)
        yield os.environ


@fixture()
def tmpdir(_fixtures: Fixtures) -> FixtureContext[Path]:
    with tempfile.TemporaryDirectory() as tempdir:
        yield Path(tempdir)


@fixture()
def popen(
    _fixtures: Fixtures, target: ModuleType = handlers.sp
) -> FixtureContext[mock.Mock]:
    with mock.patch.object(target, "Popen") as mock_obj:
        yield mock_obj


@fixture()
def acquire_sound_file(
    _fixtures: Fixtures, target: ModuleType = handlers.utils
) -> FixtureContext[mock.Mock]:
    with mock.patch.object(target, "acquire_sound_file") as mock_obj:
        yield mock_obj


@fixture()
def user_cache_path(
    _fixtures: Fixtures, target: ModuleType = utils.platformdirs
) -> FixtureContext[mock.Mock]:
    with mock.patch.object(target, "user_cache_path") as mock_obj:
        yield mock_obj


@fixture()
def event_to_speech(
    _fixtures: Fixtures, target: ModuleType = utils
) -> FixtureContext[mock.Mock]:
    with mock.patch.object(target, "event_to_speech") as mock_obj:
        yield mock_obj


@fixture()
def boto3_session(
    _fixtures: Fixtures, target: ModuleType = utils.boto3
) -> FixtureContext[mock.Mock]:
    with mock.patch.object(target, "Session") as mock_obj:
        yield mock_obj
