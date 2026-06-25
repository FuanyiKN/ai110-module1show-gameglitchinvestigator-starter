"""
A second test suite focused on scoring rules and tricky edge cases.

This complements test_game_logic.py (which targets the high/low bug).
Here we pin down update_score()'s behavior and a few parse_guess() edge
cases that are easy to get wrong.
"""

import os
import sys

# Make logic_utils importable no matter which directory pytest runs from.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from logic_utils import update_score, parse_guess, check_guess


# ---------------------------------------------------------------------------
# Scoring rules
# ---------------------------------------------------------------------------

class TestUpdateScore:
    def test_win_on_first_attempt_adds_the_most(self):
        # Earlier wins should be worth at least as much as later wins.
        early = update_score(0, "Win", attempt_number=1)
        late = update_score(0, "Win", attempt_number=5)
        assert early >= late

    def test_win_never_drops_below_floor(self):
        # The scoring caps the minimum win reward at 10 points.
        score = update_score(0, "Win", attempt_number=20)
        assert score >= 10

    def test_too_low_always_subtracts_five(self):
        assert update_score(50, "Too Low", attempt_number=1) == 45
        assert update_score(50, "Too Low", attempt_number=2) == 45

    def test_unknown_outcome_leaves_score_unchanged(self):
        # Defensive: an unexpected outcome string shouldn't change the score.
        assert update_score(42, "Sideways", attempt_number=3) == 42


# ---------------------------------------------------------------------------
# parse_guess edge cases
# ---------------------------------------------------------------------------

class TestParseGuessEdges:
    def test_negative_number_parses(self):
        ok, value, err = parse_guess("-7")
        assert ok is True
        assert value == -7

    def test_whitespace_only_string(self):
        # "   " is not a valid number.
        ok, value, err = parse_guess("   ")
        assert ok is False

    def test_none_is_rejected_gracefully(self):
        ok, value, err = parse_guess(None)
        assert ok is False
        assert value is None


# ---------------------------------------------------------------------------
# A sanity check that ties scoring + guessing together (mini "game" flow).
# ---------------------------------------------------------------------------

def test_winning_flow_increases_score():
    score = 0
    # Wrong guess (too low) loses points...
    outcome, _ = check_guess(10, 50)
    score = update_score(score, outcome, attempt_number=1)
    # ...then a correct guess should bring the score back up above zero.
    outcome, _ = check_guess(50, 50)
    score = update_score(score, outcome, attempt_number=2)
    assert outcome == "Win"
    assert score > 0
