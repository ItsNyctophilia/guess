#!/usr/bin/python3

from random import randint as rand

answer = rand(1, 99)
guess = total = invalid = 0


def pluralize(number):
    return "" if number == 1 else "es"


print(
    end=''
    f"{answer}\n"
    "I'm thinking of a number from 1 and 100\n"
    "Your guess: ")

while guess != answer:

    try:
        guess = input()
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
            f"{guess} is outside of the accepted range (1 - 100) "
            "Try again.\nYour guess: ")

    if guess > answer:
        print(
            end=''
            f"{guess} is too high. Try again.\n"
            "Your guess: ")

    elif guess < answer:
        print(
            end=''
            f"{guess} is too low. Try again.\n"
            "Your guess: ")

    else:
        print(
            f"{guess} is correct.\n"
            f"You made {total} total guess{pluralize(total)} and "
            f"{invalid} invalid guess{pluralize(invalid)}.")
