# pylint: disable=missing-docstring,unused-argument
import os
from unittest import TestCase

from gbp_testkit import fixtures as testkit
from unittest_fixtures import Fixtures, given, where

from gbp_webhook_tts import utils

EVENT = {"name": "build_pulled", "machine": "babette", "data": {}}


@given(testkit.tmpdir, user_cache_path=testkit.patch, event_to_speech=testkit.patch)
@where(user_cache_path__target="gbp_webhook_tts.utils.platformdirs.user_cache_path")
@where(event_to_speech__target="gbp_webhook_tts.utils.event_to_speech")
class AcquireSoundFileTests(TestCase):
    def test_creates_file_when_doesnot_exist(self, fixtures: Fixtures) -> None:
        fixtures.user_cache_path.return_value = fixtures.tmpdir
        fixtures.event_to_speech.return_value = b"test"

        path = utils.acquire_sound_file(EVENT)

        self.assertEqual(fixtures.tmpdir / "tts" / "babette.mp3", path)
        self.assertTrue(path.parent.is_dir())
        self.assertEqual(path.read_bytes(), b"test")

    def test_makes_path(self, fixtures: Fixtures) -> None:
        fixtures.user_cache_path.return_value = fixtures.tmpdir / "foo"
        fixtures.event_to_speech.return_value = b"test"
        path = utils.acquire_sound_file(EVENT)

        self.assertEqual(fixtures.tmpdir / "foo" / "tts" / "babette.mp3", path)
        self.assertTrue(path.parent.is_dir())
        self.assertEqual(path.read_bytes(), b"test")

    def test_returns_file_when_already_exists(self, fixtures: Fixtures) -> None:
        # Given the existing sound file for the event's machine
        fixtures.user_cache_path.return_value = fixtures.tmpdir
        existing_path = fixtures.tmpdir / "tts" / "babette.mp3"
        existing_path.parent.mkdir()
        existing_path.write_bytes(b"test")

        # When acquire_sound_file is called
        path = utils.acquire_sound_file(EVENT)

        # Then the exising file is returned
        self.assertEqual(path, existing_path)
        self.assertEqual(path.read_bytes(), b"test")


@given(testkit.tmpdir, user_cache_path=testkit.patch)
@where(user_cache_path__target="gbp_webhook_tts.utils.platformdirs.user_cache_path")
class EventToPathTests(TestCase):

    def test(self, fixtures: Fixtures) -> None:
        fixtures.user_cache_path.return_value = fixtures.tmpdir
        path = utils.event_to_path(EVENT)

        self.assertEqual(f"{fixtures.tmpdir}/tts/babette.mp3", str(path))


@given(boto3_session=testkit.patch)
@where(boto3_session__target="gbp_webhook_tts.utils.boto3.Session")
class EventToSpeechTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        text = utils.get_speech_text_for_machine("babette")
        audio = utils.event_to_speech(EVENT)

        session = fixtures.boto3_session.return_value
        session.client.assert_called_once_with("polly")
        polly = session.client.return_value
        polly.synthesize_speech.assert_called_once_with(
            VoiceId="Ivy", OutputFormat="mp3", Text=text, TextType="ssml"
        )
        speech = polly.synthesize_speech.return_value
        self.assertEqual(speech["AudioStream"].read.return_value, audio)


@given(testkit.environ)
@where(environ__clear=True)
class GetSpeechTextForMachineTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        os.environ["GBP_WEBHOOK_TTS_PHONETIC_KDE_DESKTOP"] = "foobar"

        self.assertEqual(
            ssml("foobar", 0), utils.get_speech_text_for_machine("kde-desktop")
        )

    def test_default(self, fixtures: Fixtures) -> None:
        self.assertEqual(
            ssml("kde desktop", 0), utils.get_speech_text_for_machine("kde-desktop")
        )

    def test_with_delay(self, fixtures: Fixtures) -> None:
        os.environ["GBP_WEBHOOK_TTS_DELAY"] = "0.8"

        self.assertEqual(
            ssml("kde desktop", 0.8), utils.get_speech_text_for_machine("kde-desktop")
        )


@given(testkit.environ)
@where(environ__clear=True)
class MapMachineToTextTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        os.environ["GBP_WEBHOOK_TTS_PHONETIC_KDE_DESKTOP"] = "foobar"

        self.assertEqual("foobar", utils.map_machine_to_text("kde-desktop"))

    def test_default(self, fixtures: Fixtures) -> None:
        self.assertEqual(None, utils.map_machine_to_text("kde-desktop"))


@given(testkit.environ)
@where(environ__clear=True)
class GetSoundFileTests(TestCase):
    def test(self, fixtures: Fixtures) -> None:
        os.environ["GBP_WEBHOOK_PLAYSOUND_PLAYER"] = "blahblahblah blah"

        self.assertEqual(["blahblahblah", "blah"], utils.get_sound_player())

    def test_default(self, fixtures: Fixtures) -> None:
        self.assertEqual(["pw-play"], utils.get_sound_player())


def ssml(text: str, delay: float) -> str:
    return f"""\
<speak>
  <break time="{delay}s"/>
  {text}
</speak>"""
