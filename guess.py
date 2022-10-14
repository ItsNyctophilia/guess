#!/usr/bin/python3

from random import randint as rand
from os import system, name  # geeksforgeeks.org/clear-screen-python
import sys

answer = rand(1, 99)
guess = total = invalid = 0


def pluralize(number):
    return "" if number == 1 else "es"


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


clear()
print(
    end=''
    f"{answer}\n"
    "I'm thinking of a number from 1 and 100. Type 'q' to quit \n"
    "\nYour guess: ")

while guess != answer:

    guess = input()

    if guess == "q":
        confirmation = ""
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

        print(end='' "\nYour guess: ")

    else:

        try:
            guess = int(guess)

        except ValueError:
            print(
                end='' 
                f"{guess} is not a valid guess. Try again.\n"
                "Your guess: ")
            invalid += 1
            continue

        finally:
            total += 1

        if guess < 1 or guess > 100:
            print(
                end='' 
                f"\n{guess} is outside of the accepted range"
                " (1 - 100)\n\nTry again.\n"
                "\nYour guess: ")
            invalid += 1

        else:

            if guess > answer:
                print(
                    end=''
                    f"\n{guess} is too high. Try again.\n"
                    "\nYour guess: ")

            elif guess < answer:
                print(
                    end=''
                    f"\n{guess} is too low. Try again.\n"
                    "\nYour guess: ")

            else:
                print(
                    f"{guess} is correct.\n"
                    f"You made {total} total guess{pluralize(total)} "
                    f"and {invalid} invalid guess{pluralize(invalid)}.")
