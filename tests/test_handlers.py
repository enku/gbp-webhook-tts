# pylint: disable=missing-docstring
from unittest import TestCase

import gbp_testkit.fixtures as testkit
from unittest_fixtures import Fixtures, given, where

from gbp_webhook_tts import handlers, utils


@given(acquire_sound_file=testkit.patch, sp_call=testkit.patch)
@where(sp_call__target="subprocess.call")
@where(acquire_sound_file__target="gbp_webhook_tts.handlers.utils.acquire_sound_file")
class PostPullTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        # Given the event
        event = {"name": "postpull", "machine": "babette", "data": {}}

        # When postpull is called with the event
        handlers.postpull(event)

        # Then the sound file for the event is acquired
        acquire_sound_file = fixtures.acquire_sound_file
        acquire_sound_file.assert_called_once_with(event)

        # And the sound file is played
        player = utils.get_sound_player()
        sound_file = acquire_sound_file.return_value
        sp_call = fixtures.sp_call
        sp_call.assert_called_once_with([*player, str(sound_file)])
