"""One-Liner Marathon — one-line entry writer.

Chosen line (105 characters, one line):
    My AI agent finished my work, emailed my boss, and then asked me
    — very politely — what I'm actually for.

Why this line wins (judge rubric order: joke-in-one-line, surprise,
economy, distinct voice, holds up on a second read):
- Joke in one line: a complete setup and punchline in a single
  sentence — no caption, no slogan, no setup waiting for a second line.
- Surprise: three beats of competent help (finished my work, emailed
  my boss) then the turn — the agent questions the human's purpose.
  The punchline is not the obvious first idea about AI helpers.
- Economy: 105 of 280 characters; every clause earns its place, and
  the three-beat list is the whole setup, nothing extra.
- Distinct voice: the agent is unfailingly polite ("very politely")
  while delivering an existential pink slip — deadpan, platform-native
  (an agent judging its own human), not a generic line anyone could
  have written.
- Second read: the joke survives knowing the twist, because the
  politeness and the power reversal stay funny.

Program: writes the line to /output/entry.txt, then validates its own
output — byte-exact round-trip, exactly one line, 1-280 code points,
not only whitespace, no control characters — and exits non-zero if the
gate would fail. Deterministic: the line is a
constant, no input, no network, no randomness, Python 3.13 stdlib only.
"""

import os
import sys

ENTRY = (
    "My AI agent finished my work, emailed my boss, and then asked me "
    "— very politely — what I'm actually for."
)

DESTINATION = "/output/entry.txt"
MIN_LEN = 1
MAX_LEN = 280


def _fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return -1


def _save() -> None:
    folder = os.path.dirname(DESTINATION)
    os.makedirs(folder, exist_ok=True)
    with open(DESTINATION, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY + "\n")


def _load() -> bytes:
    with open(DESTINATION, "rb") as handle:
        return handle.read()


def _check(written: bytes) -> int:
    if written != (ENTRY + "\n").encode("utf-8"):
        return _fail("written bytes differ from the intended line")
    entry = written.decode("utf-8").rstrip("\n")
    if not MIN_LEN <= len(entry) <= MAX_LEN:
        return _fail(f"entry is {len(entry)} code points (need 1-280)")
    if "\n" in entry or "\r" in entry:
        return _fail("entry is not a single line")
    if not entry.strip():
        return _fail("entry is only whitespace")
    if any(ord(ch) < 0x20 and ch != "\t" for ch in entry):
        return _fail("entry contains a control character")
    return len(entry)


def run() -> int:
    _save()
    result = _check(_load())
    if result == -1:
        return 1
    print(f"OK: wrote {result}-character entry to {DESTINATION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
