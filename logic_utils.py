# FIX: Refactored this function out of app.py into logic_utils.py using AI agent mode.
# Fixme (fixed): Normal and Hard ranges were swapped (Normal was 1-100, Hard was 1-50).
# Normal is now 1-50 and Hard is now 1-100 so Hard is actually the wider/harder range.
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


# FIX: AI located the flipped if/else conditions; I verified the hint direction in-game.
# Fixme (fixed): the Go LOWER / Go HIGHER hints were reversed.
# A guess HIGHER than the secret ("Too High") must tell the player to go LOWER,
# and a guess LOWER than the secret ("Too Low") must tell them to go HIGHER.
# Also removed the fragile str()-comparison fallback (see app.py) that hid this bug.
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIX: AI spotted an off-by-one in the win bonus (was 100 - 10*(attempt_number+1)),
        # which I confirmed by checking that a first-guess win scored 80 instead of 90.
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    # FIX: AI flagged that "Too High" gave +5 on even attempts, rewarding a wrong guess.
    # I verified in-game (score went UP after a too-high guess) and made both wrong
    # outcomes lose 5 points, matching "Too Low".
    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
