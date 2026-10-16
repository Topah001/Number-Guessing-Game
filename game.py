"""An interactive number guessing game."""

from __future__ import annotations

import random
from collections.abc import Callable

MIN_NUMBER = 1
MAX_NUMBER = 100
DIFFICULTY_RANGES = {
    "easy": (1, 25),
    "medium": (1, 50),
    "hard": (1, 100),
}


def choose_number(min_number: int = MIN_NUMBER, max_number: int = MAX_NUMBER) -> int:
    """Choose a secret number within the configured range."""
    if min_number > max_number:
        raise ValueError("min_number must be less than or equal to max_number.")
    return random.randint(min_number, max_number)


def get_difficulty_range(level: str) -> tuple[int, int]:
    """Return the numeric range for a difficulty level."""
    normalized = level.strip().lower()
    if normalized not in DIFFICULTY_RANGES:
        valid_levels = ", ".join(sorted(DIFFICULTY_RANGES))
        raise ValueError(f"Difficulty must be one of: {valid_levels}.")
    return DIFFICULTY_RANGES[normalized]


def get_hint(guess: int, secret_number: int) -> str:
    """Return feedback for a guess."""
    if guess < secret_number:
        return "Too low! Try a higher number."
    if guess > secret_number:
        return "Too high! Try a lower number."
    return "Correct!"


def parse_guess(
    guess_input: str,
    min_number: int = MIN_NUMBER,
    max_number: int = MAX_NUMBER,
) -> int:
    """Convert a raw input value into a valid integer guess."""
    try:
        guess = int(guess_input.strip())
    except ValueError as exc:
        raise ValueError("Please enter a whole number.") from exc

    if not min_number <= guess <= max_number:
        raise ValueError(f"Choose a number between {min_number} and {max_number}.")

    return guess


def play_round(
    secret_number: int | None = None,
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
    min_number: int = MIN_NUMBER,
    max_number: int = MAX_NUMBER,
) -> int:
    """Run one guess round and return the number of attempts used."""
    if secret_number is None:
        secret_number = choose_number(min_number, max_number)

    attempts = 0
    output_func(f"\nI'm thinking of a number from {min_number} to {max_number}.")

    while True:
        try:
            guess = parse_guess(input_func("Your guess: "), min_number, max_number)
        except ValueError as exc:
            output_func(str(exc))
            continue

        attempts += 1
        hint = get_hint(guess, secret_number)
        output_func(hint)
        if guess == secret_number:
            output_func(f"You got it in {attempts} {'guess' if attempts == 1 else 'guesses'}!")
            return attempts


def main() -> None:
    """Run the full game loop."""
    print("Number Guessing Game")
    total_score = 0
    while True:
        try:
            difficulty = input("Choose difficulty (easy/medium/hard): ").strip().lower()
            min_number, max_number = get_difficulty_range(difficulty)
        except ValueError as exc:
            print(exc)
            continue

        attempts = play_round(min_number=min_number, max_number=max_number)
        total_score += max(0, 10 - attempts + 1)
        print(f"Current score: {total_score}")

        if input("\nPlay again? (y/n): ").strip().lower() not in {"y", "yes"}:
            print("Thanks for playing!")
            return


if __name__ == "__main__":
    main()
