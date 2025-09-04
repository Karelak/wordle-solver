import json
import random
from typing import List


class WordleSolver:
    """A class to solve Wordle puzzles by managing game state and word filtering."""

    def __init__(self, word_file: str = "validwords.json"):
        """Initialize the Wordle solver with a word list."""
        self.words = self._load_words(word_file)
        self.green_letters = {0: "", 1: "", 2: "", 3: "", 4: ""}
        self.yellow_letters = []  # List of [letter, position] pairs
        self.gray_letters = []  # List of letters that aren't in the word

    def _load_words(self, filename: str) -> List[str]:
        """Load words from JSON file and convert to uppercase."""
        with open(filename) as f:
            words = json.load(f)
        return [word.upper() for word in words]

    def get_initial_guess(self) -> str:
        """Get a random initial guess from the word list."""
        return random.choice(self.words)

    def get_user_feedback(self, guess: str) -> None:
        """Get user feedback for each letter in the guess and update game state."""
        current_pos = 0

        while current_pos < 5:
            status = int(
                input(
                    f"What colour is letter {guess[current_pos]} of word {guess}? \n"
                    " 1 - Green \n 2 - Yellow \n 3 - Gray \n"
                )
            )

            letter = guess[current_pos]

            if status == 1:  # Green
                self.green_letters[current_pos] = letter
            elif status == 2:  # Yellow
                self.yellow_letters.append([letter, current_pos])
            elif status == 3:  # Gray
                self.gray_letters.append(letter)

            current_pos += 1

    def _is_word_valid(self, word: str) -> bool:
        """Check if a word matches all the current constraints."""
        # Check gray letters (letters not in the word)
        for letter in self.gray_letters:
            if letter in word:
                return False

        # Check green letters (correct position)
        for pos, letter in self.green_letters.items():
            if letter != "" and word[pos] != letter:
                return False

        # Check yellow letters (in word but wrong position)
        for letter, bad_pos in self.yellow_letters:
            if letter not in word or word[bad_pos] == letter:
                return False

        return True

    def get_next_guess(self) -> str:
        """Get the next guess based on current constraints."""
        valid_words = [word for word in self.words if self._is_word_valid(word)]

        if not valid_words:
            raise ValueError("No valid words found with current constraints!")

        return random.choice(valid_words)

    def is_solved(self) -> bool:
        """Check if the puzzle is solved (all positions have green letters)."""
        return "" not in self.green_letters.values()

    def reset_game_state(self) -> None:
        """Reset the game state for a new puzzle."""
        self.green_letters = {0: "", 1: "", 2: "", 3: "", 4: ""}
        self.yellow_letters = []
        self.gray_letters = []

    def solve(self) -> None:
        """Main method to solve a Wordle puzzle interactively."""
        # Get initial guess
        first_guess = input("Initial guess if you already put something in: ").upper()
        if not first_guess:
            first_guess = self.get_initial_guess()

        print(f"Using guess: {first_guess}")
        self.get_user_feedback(first_guess)

        # Continue guessing until solved
        while not self.is_solved():
            try:
                guess = self.get_next_guess()
                print(f"Next guess: {guess}")
                self.get_user_feedback(guess)
            except ValueError as e:
                print(f"Error: {e}")
                break

        if self.is_solved():
            solution = "".join(self.green_letters.values())
            print(f"Puzzle solved! The word is: {solution}")


if __name__ == "__main__":
    solver = WordleSolver()
    solver.solve()
