"""
Stickman — a small terminal animation.

The original (stickman_fail.py) tried to animate a walking stick figure by
counting "move cursor up N lines" escape codes by hand, but the draw and
erase phases printed different numbers of lines, so the frames never lined
up and the animation didn't actually work. This version clears the whole
screen each frame instead (`\\033c`) and alternates two leg poses to fake a
walking motion — simpler, and it actually walks.

Not tied to any of your other projects — MONTY calls this as a fun
easter-egg command, and it also runs standalone: `python stickman.py`.
"""

import shutil
import sys
import time

# Two leg poses, alternated each frame for a walking effect.
_POSE_A = [
    " o ",
    "/|\\",
    "/ \\",
]
_POSE_B = [
    " o ",
    "/|\\",
    " |\\",
]


def _frame(pose, indent):
    return "\n".join((" " * indent) + line for line in pose)


def play(steps=20, delay=0.12, stream=sys.stdout):
    """Walk a stickman across the terminal. `steps` frames, `delay` seconds each."""
    width = shutil.get_terminal_size(fallback=(80, 24)).columns
    max_indent = max(width - 6, 1)

    for i in range(steps):
        indent = int((i / max(steps - 1, 1)) * max_indent)
        pose = _POSE_A if i % 2 == 0 else _POSE_B
        stream.write("\033c")  # full screen clear/reset — avoids manual cursor math
        stream.write(_frame(pose, indent) + "\n")
        stream.flush()
        time.sleep(delay)


if __name__ == "__main__":
    play()
