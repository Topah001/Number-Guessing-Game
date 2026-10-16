import pytest

import game


def test_choose_number_is_in_range():
    for _ in range(100):
        value = game.choose_number()
        assert game.MIN_NUMBER <= value <= game.MAX_NUMBER


def test_get_difficulty_range_accepts_supported_levels():
    assert game.get_difficulty_range("easy") == (1, 25)
    assert game.get_difficulty_range("medium") == (1, 50)
    assert game.get_difficulty_range("hard") == (1, 100)

    with pytest.raises(ValueError, match="Difficulty must be one of"):
        game.get_difficulty_range("impossible")


def test_get_hint_cases():
    assert game.get_hint(10, 20) == "Too low! Try a higher number."
    assert game.get_hint(30, 20) == "Too high! Try a lower number."
    assert game.get_hint(20, 20) == "Correct!"


def test_parse_guess_validates_input():
    assert game.parse_guess("25") == 25
    with pytest.raises(ValueError, match="whole number"):
        game.parse_guess("abc")
    with pytest.raises(ValueError, match="Choose a number"):
        game.parse_guess("0")
    with pytest.raises(ValueError, match="Choose a number"):
        game.parse_guess("101")


def test_play_round_returns_attempts_and_handles_correct_guess():
    calls = iter(["50", "30"])
    output = []

    attempts = game.play_round(secret_number=30, input_func=lambda _: next(calls), output_func=output.append)

    assert attempts == 2
    assert any("You got it in 2 guesses!" == line for line in output)


def test_play_round_respects_custom_range():
    calls = iter(["10", "7"])
    output = []

    attempts = game.play_round(
        secret_number=7,
        input_func=lambda _: next(calls),
        output_func=output.append,
        min_number=1,
        max_number=10,
    )

    assert attempts == 2
    assert any(line.startswith("\nI'm thinking of a number from 1 to 10.") for line in output)
