#!/usr/bin/python3
"""Interactive high-low number guessing game

Prompts the user for a number and checks it against a
randomly-generated integer between 1 and 100, telling them
if they are too high, too low, or got the correct answer"""

from random import randint as rand
from os import system, name
from os.path import exists
import sys


def pluralize(number):
    """Pluralizes given word that normally ends in 'es' when plural

    Arguments:
    number -- number check word pluralization for
    Returns:
    '' or 'es' if the word should be plural"""

    return "" if number == 1 else "es"


def clear():  # geeksforgeeks.org/clear-screen-python
    """Clears the screen"""

    if name == 'nt':
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

        while confirmation != "n":
            confirmation = input()

            if confirmation == "y":
                clear()
                sys.exit()

            elif confirmation != "n":
                clear()
                print(
                    end=''
                    "Invalid response.\n"
                    "\nAre you sure you would like to quit?\n"
                    "\n(y/n): ")

        clear()
        print(end='' "Resuming. . .\n")

        # Below checks if lastguess was instantiated as a nonzero value
        # by a valid guess. If it was, tell the user if their last
        # guess was too low or too high, otherwise, repeat the
        # introductory message.
        if lastguess:
            if lastguess > answer:
                print(f"Your last guess {lastguess} was too high")
            else:
                print(f"Your last guess {lastguess} was too low")
        else:
            print(
                "I'm thinking of a number from 1 and 100. "
                "Type 'q' to quit")
        print(end='' "\nYour guess: ")

    return True if confirmation else False


class Save:

    def __init__(self, user, total_games, total_guess, invalid_guess):
        self.user = user
        self.total_games = total_games
        self.total_guess = total_guess
        self.invalid_guess = invalid_guess

    def show(self):
        print(
            f"You have played {self.total_games} game overall, "
            f"have made {self.total_guess} total "
            f"guess{pluralize(self.total_guess)}, "
            f"and {self.invalid_guess} invalid "
            f"guess{pluralize(self.invalid_guess)}.")

    def update(self, current_guess, current_invalid):
        self.total_games += 1
        self.total_guess += current_guess
        self.invalid_guess += current_invalid


answer = rand(1, 100)  # Instantiate computer's starting number as
# random integer from 1 to 100.
lastguess = guess = total = invalid = 0  # Instantiate multiple
# variables to be used later using 0 as a placeholder.

print(
    end=''
    "Please enter your name.\n"
    "\nName: ")

player_name = input()

# Add fancy code reading existing number values from file and
# unpacking them into the object here

if exists("./.guess_saves"):
    with open(".guess_saves", "r+") as fo:

        found_match = False
        content = fo.read().splitlines()
        print(content)

        for line in content:

            line = line.split(",")

            if player_name == line[0]:
                current_player = Save(
                    player_name, int(line[1]),
                    int(line[2]), int(line[3]))
                found_match = True
                break

        if not found_match:
            fo.write(player_name + ",0,0,0")
            current_player = Save(player_name, 0, 0, 0)


print(
    end=''
    f"{answer}\n"
    "I'm thinking of a number from 1 and 100. Type 'q' to quit \n"
    "\nYour guess: ")


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

        if guess < 1 or guess > 100:  # Check if guess in 1 - 100 range
            print(
                end='' 
                f"\n{guess} is outside of the accepted range"
                " (1 - 100). Try again.\n"
                "\nYour guess: ")
            invalid += 1

        else:

            if guess > answer:  # Case: user guess too high
                print(
                    end=''
                    f"\n{guess} is too high. Try again.\n"
                    "\nYour guess: ")

            elif guess < answer:  # Case: user guess too low
                print(
                    end=''
                    f"\n{guess} is too low. Try again.\n"
                    "\nYour guess: ")

            lastguess = guess  # save value of guess as lastguess in
            # case the user starts quitting and the screen is cleared

print(
    f"{guess} is correct.\n"
    f"This game, you made {total} total guess{pluralize(total)} "
    f"and {invalid} invalid guess{pluralize(invalid)}.")

current_player.update(total, invalid)
current_player.show()
