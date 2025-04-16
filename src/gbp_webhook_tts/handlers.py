"""gbp-webhook handler"""

import subprocess as sp
from typing import Any

from . import utils


def build_pulled(event: dict[str, Any]) -> None:
    """build_pulled event handler"""
    sound_file = utils.acquire_sound_file(event)
    args = ["pw-play", str(sound_file)]

    sp.Popen(args)  # pylint: disable=consider-using-with
