"""
Tests for Game Glitch Investigator logic.

These target the bugs we fixed during the lab:

  Bug 1 — Backwards high/low hints (TESTABLE here).
          check_guess() is a pure function in logic_utils.py, so we can
          assert its outcome/message directly.

  Bug 2 — Pressing Enter did not submit the guess (NOT unit-testable here).
          This was a Streamlit widget behavior (a plain st.button only fires
          on click). The fix was wrapping the input in an st.form so Enter
          triggers st.form_submit_button. It lives in app.py's UI layer and
          requires the Streamlit runtime / a browser to exercise.

  Bug 3 — "New Game" did not reset the game (NOT unit-testable here).
          The handler failed to reset st.session_state.status, so the app
          stayed on the game-over screen. The fix lives inline in app.py and
          mutates st.session_state, which isn't a pure function. See the note
          at the bottom for how it COULD be made testable.
"""

import os
import sys

# Make logic_utils importable when pytest runs the test from the test/ dir.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from logic_utils import (
    check_guess,
    parse_guess,
    update_score,
    get_range_for_difficulty,
)


# ---------------------------------------------------------------------------
# Bug 1: high/low hints must point the player in the RIGHT direction.
# ---------------------------------------------------------------------------

class TestCheckGuessDirection:
    def test_guess_too_high_says_go_lower(self):
        outcome, message = check_guess(80, 50)
        assert outcome == "Too High"
        assert "LOWER" in message  # the bug used to say "HIGHER" here

    def test_guess_too_low_says_go_higher(self):
        outcome, message = check_guess(20, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in message  # the bug used to say "LOWER" here

    def test_correct_guess_wins(self):
        outcome, message = check_guess(50, 50)
        assert outcome == "Win"

    @pytest.mark.parametrize(
        "guess, secret, expected",
        [
            (71, 9, "Too High"),   # from the reflection bug-repro log
            (25, 11, "Too High"),  # from the reflection bug-repro log
            (15, 28, "Too Low"),   # from the reflection bug-repro log
            (1, 100, "Too Low"),
            (100, 1, "Too High"),
        ],
    )
    def test_direction_from_repro_log(self, guess, secret, expected):
        outcome, _ = check_guess(guess, secret)
        assert outcome == expected

    def test_string_secret_bug(self):
        # Bug 4: guesses BELOW the secret used to say "Go LOWER" because the
        # secret was compared as text ("5" > "10"). With a numeric secret,
        # single-digit guesses below a two-digit secret must read "Too Low".
        assert check_guess(5, 10)[0] == "Too Low"
        assert check_guess(2, 10)[0] == "Too Low"
        assert check_guess(9, 10)[0] == "Too Low"

    def test_messages_are_never_contradictory(self):
        # A "Too High" outcome must never tell the player to go higher,
        # and vice versa -- this is the exact mistake the original bug made.
        high_outcome, high_msg = check_guess(90, 10)
        low_outcome, low_msg = check_guess(10, 90)
        assert "HIGHER" not in high_msg
        assert "LOWER" not in low_msg


# ---------------------------------------------------------------------------
# Supporting logic (parse_guess, update_score, get_range_for_difficulty).
# Not the headline bugs, but they protect the refactor into logic_utils.py.
# ---------------------------------------------------------------------------

class TestParseGuess:
    def test_valid_integer(self):
        assert parse_guess("42") == (True, 42, None)

    def test_float_is_truncated_to_int(self):
        ok, value, err = parse_guess("3.9")
        assert ok is True
        assert value == 3

    def test_empty_string_is_rejected(self):
        ok, value, err = parse_guess("")
        assert ok is False
        assert value is None
        assert err

    def test_non_number_is_rejected(self):
        ok, value, err = parse_guess("abc")
        assert ok is False
        assert err == "That is not a number."


class TestGetRangeForDifficulty:
    @pytest.mark.parametrize(
        "difficulty, expected",
        [
            ("Easy", (1, 20)),
            ("Normal", (1, 100)),
            ("Hard", (1, 50)),
            ("Unknown", (1, 100)),  # falls back to default
        ],
    )
    def test_ranges(self, difficulty, expected):
        assert get_range_for_difficulty(difficulty) == expected


class TestUpdateScore:
    def test_loss_directions_subtract(self):
        # "Too Low" always loses 5 points.
        assert update_score(50, "Too Low", attempt_number=3) == 45

    def test_win_adds_points(self):
        # A win should never decrease the score.
        assert update_score(0, "Win", attempt_number=1) > 0


# ---------------------------------------------------------------------------
# NOTE on Bug 3 (New Game reset):
#
# The reset logic currently lives inline in app.py and mutates
# st.session_state directly, so it can't be imported and tested in isolation.
# To make it testable, you'd extract a pure helper into logic_utils.py, e.g.:
#
#     def new_game_state(low, high, secret):
#         return {"attempts": 1, "secret": secret,
#                 "status": "playing", "score": 0, "history": []}
#
# then app.py would call it and assign the result into st.session_state, and a
# test could assert new_game_state(...)["status"] == "playing". Bug 2 (Enter
# submitting) is pure UI and would need a Streamlit end-to-end test instead.
# ---------------------------------------------------------------------------
