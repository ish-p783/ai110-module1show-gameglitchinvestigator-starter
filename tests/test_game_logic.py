from logic_utils import (
    check_guess,
    parse_guess,
    get_range_for_difficulty,
    update_score,
)

# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

# Targets the bug we fixed: the Go LOWER / Go HIGHER hints were reversed.
def test_too_high_tells_player_to_go_lower():
    # A guess above the secret must tell the player to go LOWER
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_tells_player_to_go_higher():
    # A guess below the secret must tell the player to go HIGHER
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------

def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_range_normal():
    # Targets the swapped-range bug: Normal must be 1-50, not 1-100
    assert get_range_for_difficulty("Normal") == (1, 50)

def test_range_hard():
    # Targets the swapped-range bug: Hard must be 1-100, not 1-50
    assert get_range_for_difficulty("Hard") == (1, 100)

def test_range_unknown_defaults_to_1_100():
    assert get_range_for_difficulty("Whatever") == (1, 100)

# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_decimal_is_truncated_to_int():
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7

def test_parse_empty_string_is_rejected():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_none_is_rejected():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None

def test_parse_non_number_is_rejected():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."

# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

def test_win_on_first_guess_awards_90():
    # attempt_number == 1 -> 100 - 10*1 = 90 (off-by-one in the bonus is fixed)
    assert update_score(0, "Win", 1) == 90

def test_win_bonus_decreases_with_more_attempts():
    assert update_score(0, "Win", 3) == 70

def test_win_bonus_never_below_10():
    # A very late win still awards the floor of 10 points
    assert update_score(0, "Win", 99) == 10

def test_too_high_always_loses_5():
    # Targets the scoring bug: a wrong guess must never ADD points,
    # on even or odd attempts.
    assert update_score(100, "Too High", 2) == 95
    assert update_score(100, "Too High", 3) == 95

def test_too_low_loses_5():
    assert update_score(100, "Too Low", 2) == 95
