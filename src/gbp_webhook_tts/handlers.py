"""gbp-webhook handler"""

import os
import subprocess as sp
import time
from typing import Any

from . import utils


def build_pulled(event: dict[str, Any]) -> None:
    """build_pulled event handler"""
    sound_file = utils.acquire_sound_file(event)
    args = ["pw-play", str(sound_file)]

    environ = os.environ
    time.sleep(float(environ.get("GBP_WEBHOOK_TTS_DELAY", "0")))

    sp.Popen(args)  # pylint: disable=consider-using-with
