"""gbp-webhook handler"""

import subprocess as sp
from typing import Any

from . import utils


def postpull(event: dict[str, Any]) -> None:
    """postpull event handler"""
    with sp.Popen([*utils.get_sound_player(), str(utils.acquire_sound_file(event))]):
        pass
