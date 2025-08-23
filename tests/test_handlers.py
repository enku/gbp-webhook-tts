# pylint: disable=missing-docstring
from unittest import TestCase, mock

import gbp_testkit.fixtures as testkit
from unittest_fixtures import Fixtures, given, where

from gbp_webhook_tts import handlers, utils


@given(acquire_sound_file=testkit.patch, popen=testkit.patch)
@where(popen__target="subprocess.Popen")
@where(acquire_sound_file__target="gbp_webhook_tts.handlers.utils.acquire_sound_file")
class BuildPulledTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        # Given the event
        event = {"name": "build_pulled", "machine": "babette", "data": {}}

        # When build_pulled is called with the event
        handlers.build_pulled(event)

        # Then the sound file for the event is acquired
        acquire_sound_file: mock.Mock = fixtures.acquire_sound_file
        acquire_sound_file.assert_called_once_with(event)

        # And the sound file is played
        player = utils.get_sound_player()
        sound_file = acquire_sound_file.return_value
        popen_cls: mock.Mock = fixtures.popen
        popen_cls.assert_called_once_with([*player, str(sound_file)])
