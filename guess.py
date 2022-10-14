#!/usr/bin/python3
"""Interactive high-low number guessing game.

Prompts the user for a number and checks it against a
randomly-generated integer between 1 and 100, telling them
if they are too high, too low, or got the correct answer. Saves
data from previous games and displays statistics for each user."""

from random import randint as rand
from os import system, name
from os.path import exists
import sys

answer = rand(1, 100)  # Instantiate computer's starting number as
# random integer from 1 to 100.
last_guess = guess = total = invalid = 0
current_player = None


def pluralize(number):
    """Pluralizes given word that normally ends in 'es' when plural.

    Arguments:
    number -- number check word pluralization for
    Returns:
    '' or 'es' if the word should be plural"""

    return "" if number == 1 else "es"


def clear():  # geeksforgeeks.org/clear-screen-python
    """Clears the screen"""

    if name == 'nt':  # If on Windows machine.
        system('cls')
    else:
        system('clear')


def quitcheck(userinput):
    """Checks if the user started the quitting process by typing 'q'

    Arguments:
    userinput -- the user's guess from the current game round
    Returns:
    True if the user tried to quit, otherwise False"""

    confirmation = ""  # Instantiates 'confirmation' as an empty string
    # so that if the user did not start the quitting process,
    # the function returns False.

    if userinput == "q":

        clear()
        print(
            end=''
            "Are you sure you would like to quit?\n"
            "(Your current game stats will not be saved)\n"
            "\n(y/n): ")

        while confirmation != "n":  # Exit loop if user types "n" to
            # decline quitting.

            confirmation = input()

            if confirmation == "y":  # User confirmed quit, exit.

                clear()
                sys.exit()

            elif confirmation != "n":  # Input was neither n nor y,
                # inform user of error.

                clear()
                print(
                    end=''
                    "Invalid response.\n"
                    "\nAre you sure you would like to quit?\n"
                    "\n(y/n): ")

        clear()
        print(end='' "Resuming. . .\n")

        # Below checks if last_guess was instantiated as a nonzero value
        # by a valid guess. If it was, tell the user if their last
        # guess was too low or too high, otherwise, repeat the
        # introductory message.
        if last_guess:

            if last_guess > answer:

                print(f"Your last guess {last_guess} was too high")

            else:

                print(f"Your last guess {last_guess} was too low")

        else:

            print(
                "I'm thinking of a number from 1 and 100. "
                "Type 'q' to quit")

        print(end='' "\nYour guess: ")

    return True if confirmation else False


def save_game():
    """Saves current game statistics to .guess_saves.

    Reads content of existing saves file to 'all_content', then
    manipulates it so the name value can be compared to the current
    user's entered name, overwriting existing statistics with the
    new ones if they match."""

    with open(".guess_saves", "r") as fo:

        all_content = fo.read()
        all_content = all_content.splitlines()

    with open(".guess_saves", "w") as fo:

        for line in all_content:

            if player_name == line.split(",")[0]:

                fo.writelines(current_player.print_save_string())
                # Overwrite existing data with new data if the user's
                # name value in file matches the current user's name as
                # stored in the current_player object.
                fo.write("\n")

            else:

                fo.writelines(line)
                # Otherwise, write the existing line as-is.
                fo.write("\n")


def load_game():
    """Attempts to load saved statistics from .guess_saves.

    Checks if .guess_saves exist and creates it if not, reading line
    by line looking for a line with a user's name that matches the
    one provided as 'player_name', loading the saved data into the
    object current_player, if possible. If no name matches, creates a
    new entry for that user. """

    global current_player

    if exists(".guess_saves"):  # Verify that .guess_saves exists

        with open(".guess_saves", "r+") as fo:

            found_match = False
            content = fo.read().splitlines()

            for line in content:

                line = line.split(",")

                if player_name == line[0]:

                    current_player = SaveData(
                        player_name, int(line[1]),
                        int(line[2]), int(line[3]))
                    found_match = True
                    break

            if not found_match:

                fo.write(player_name + ",0,0,0")
                current_player = SaveData(player_name, 0, 0, 0)

    else:

        with open(".guess_saves", "w") as fo:

            fo.write(player_name + ",0,0,0")
            current_player = SaveData(player_name, 0, 0, 0)


class SaveData:
    """A class representing the save data for an individual user.

    Attributes
    ----------
    user : str
        name of save file
    total_games : int
        number of total games the user has played
    total_guess : int
        number of total valid or invalid guesses the user has provided
    invalid_guess : int
        number of invalid guesses the user has provided

    Methods
    -------
    running_total()
        prints the user's statistics across all games played
    update(current_guess, current_invalid)
        updates the user's overall totals with the current
        game's values for games played and total / invalid guesses
    print_save_string()
        returns a string formatted properly for use by the save_game()
        function."""

    def __init__(self, user, total_games, total_guess, invalid_guess):
        """Constructs necessary attributes for the SaveData object.

        Parameters
        ----------
            user : str
                name of save file
            total_games : int
                number of total games the user has played
            total_guess : int
                number of total valid or invalid guesses the user
                has provided
            invalid_guess : int
                number of invalid guesses the user has provided"""

        self.user = user
        self.total_games = total_games
        self.total_guess = total_guess
        self.invalid_guess = invalid_guess

    def running_total(self):
        """Prints the user's statistics across all games played."""

        # stackoverflow.com/questions/21872366 for the trick on line
        # 103 for formatting the plural of 'game'
        print(
            f"You have played {self.total_games} "
            f"game{'s'[:self.total_games != 1]} overall, " 
            f"have made {self.total_guess} total "
            f"guess{pluralize(self.total_guess)}, "
            f"and {self.invalid_guess} invalid "
            f"guess{pluralize(self.invalid_guess)}.\n"
            "\nOn average, you take "
            f"{self.total_guess / self.total_games:.2f} "
            f"guess{pluralize(self.total_guess / self.total_games)} to "
            "guess my number.")

    def update(self, current_guess, current_invalid):
        """Update overall statistics with current game's.

        Parameters
        ----------
        current_guess : int
            number of total guesses from current game
        current_invalid : int
            number of total invalid guesses from current game

        Returns
        -------
        None"""

        self.total_games += 1
        self.total_guess += current_guess
        self.invalid_guess += current_invalid

    def print_save_string(self):
        """Prints a string for save_game() to output to a file."""

        return(
            f"{self.user},{self.total_games},"
            f"{self.total_guess},{self.invalid_guess}")


# This loop is for ensuring the player enters a valid name,
# at which point it will attempt to load any saved stats they have,
# and if there is no entry for that player, load_game will create a
# new one.
while True:

    clear()

    print(
        end=''
        "Please enter your name. (Case sensitive)\n"
        "\nName: ")

    player_name = input()

    if player_name.isalpha():  # Valid names are exclusively
        # alphabetical with no spaces, for ease of storage.

        load_game()
        clear()
        break

    else:

        clear()
        print("Names may only contain alphabetical "
              "characters and no spaces.\n"
              "\nPress enter to continue.")
        input()

print(
    end=''
    f"{player_name}, I'm thinking of a number from 1 and 100. "
    "Type 'q' to quit.\n\nYour guess: ")

while guess != answer:

    guess = input()  # Gather user input

    if not quitcheck(guess):  # If the user tried to quit, guess == 'q',
        # don't try to check if their input is valid.

        # If user string can be turned into an integer, it's valid
        # input, continue as normal, otherwise, catch the ValueError,
        # inform the user, and increment the invalid guess counter

        try:

            guess = int(guess)

        except ValueError:

            print(
                end='' 
                f"\n{guess} is not a valid guess. Try again.\n"
                "\nYour guess: ")
            invalid += 1
            continue

        finally:

            total += 1

        if guess < 1 or guess > 100:  # Check if guess in 1 - 100
            # range, incrementing invalid guess counter if it is.

            print(
                end='' 
                f"\n{guess} is outside of the accepted range"
                " (1 - 100). Try again.\n"
                "\nYour guess: ")
            invalid += 1

        else:  # if user's input is valid, test it against 'answer'

            if guess > answer:  # Case: user guess is too high

                print(
                    end=''
                    f"\n{guess} is too high. Try again.\n"
                    "\nYour guess: ")

            elif guess < answer:  # Case: user guess is too low

                print(
                    end=''
                    f"\n{guess} is too low. Try again.\n"
                    "\nYour guess: ")

            last_guess = guess  # save value of guess as last_guess in
            # case the user starts quitting and the screen is cleared

# Once user wins, print current game statistics, update running
# statistics, save game to file, and output running total.
print(
    f"\n{guess} is correct.\n"
    f"\nThis game, you made {total} total guess{pluralize(total)} "
    f"and {invalid} invalid guess{pluralize(invalid)}.\n")

current_player.update(total, invalid)
save_game()
current_player.running_total()
