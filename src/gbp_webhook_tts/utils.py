"""gbp-webhook-tts utils"""

from pathlib import Path
from typing import Any

import boto3
import platformdirs


def acquire_sound_file(event: dict[str, Any]) -> Path:
    """Acquire the audio file needed for the event and return the path"""
    path: Path = event_to_path(event)
    if not path.exists():
        audio = event_to_speech(event)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(audio)
    return path


def event_to_path(event: dict[str, Any]) -> Path:
    """Given the path return the pathname of the audio file"""
    machine = event["machine"]
    dirname = platformdirs.user_cache_path("gbp-webhook") / "tts"

    return dirname / f"{machine}.mp3"


def event_to_speech(event: dict[str, Any]) -> bytes:
    """Return .mp3 audio for the given event"""
    text = event["machine"].replace("-", " ")
    polly = boto3.Session().client("polly")
    response = polly.synthesize_speech(VoiceId="Ivy", OutputFormat="mp3", Text=text)

    return response["AudioStream"].read()
