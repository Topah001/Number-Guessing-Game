"""An interactive number guessing game."""

import random


MIN_NUMBER = 1
MAX_NUMBER = 100


def choose_number() -> int:
    """Choose a secret number within the game's range."""
    return random.randint(MIN_NUMBER, MAX_NUMBER)


def get_hint(guess: int, secret_number: int) -> str:
    """Return feedback for a guess."""
    if guess < secret_number:
        return "Too low! Try a higher number."
    if guess > secret_number:
        return "Too high! Try a lower number."
    return "Correct!"


def play_round() -> None:
    secret_number = choose_number()
    attempts = 0

    print(f"\nI'm thinking of a number from {MIN_NUMBER} to {MAX_NUMBER}.")
    while True:
        guess_input = input("Your guess: ").strip()
        try:
            guess = int(guess_input)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if not MIN_NUMBER <= guess <= MAX_NUMBER:
            print(f"Choose a number between {MIN_NUMBER} and {MAX_NUMBER}.")
            continue

        attempts += 1
        hint = get_hint(guess, secret_number)
        print(hint)
        if guess == secret_number:
            print(f"You got it in {attempts} {'guess' if attempts == 1 else 'guesses'}!")
            return


def main() -> None:
    print("Number Guessing Game")
    while True:
        play_round()
        if input("\nPlay again? (y/n): ").strip().lower() not in {"y", "yes"}:
            print("Thanks for playing!")
            return


if __name__ == "__main__":
    main()
