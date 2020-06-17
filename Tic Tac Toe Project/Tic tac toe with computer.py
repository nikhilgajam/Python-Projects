import random

print(" Welcome To Tic Tac Toe Game\n")

user = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
comp = [0, 1, 2, 3, 4, 5, 6, 7, 8]
random.shuffle(comp)  # We are shuffling the numbers at the starting
x = o = 0

'''

Game Logic Explanation

We will have a list of numbers when you or computer enters a number that number will be removed from the list
because we cannot place two things in a same box and also we should not access same box again
then there are conditions to check who won the game. All these things will work with random
numbers picked by computer

'''


def board():
    print(user[0] + " | " + user[1] + " | " + user[2])
    print("--+---+--")
    print(user[3] + " | " + user[4] + " | " + user[5])
    print("--+---+--")
    print(user[6] + " | " + user[7] + " | " + user[8])
    print()


board()

while True:
    # User input with error check
    try:
        x = int(input("Enter (1-9) numbers: "))
    except ValueError:
        print("Enter only numbers")

    if x not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        print("Enter numbers 1-9")
        continue

    try:
        # Removing the number entered by user
        comp.remove(x-1)

        try:
            # Random number picking
            o = random.choice(comp)

        except IndexError:
            # Index error will arise when no numbers remain that means it is a tie
            user[o] = "O"
            board()
            print("Tie")
            break

        # Removing the numbers entered by computer
        comp.remove(o)

    except ValueError:
        print("Enter number of empty box")
        continue

    user[x-1] = "X"
    user[o] = "O"

    board()

    # User board check

    if user[0] == user[1] == user[2] == "X":
        print("You Won The Game")
        break

    elif user[3] == user[4] == user[5] == "X":
        print("You Won The Game")
        break

    elif user[6] == user[7] == user[8] == "X":
        print("You Won The Game")
        break

    elif user[0] == user[3] == user[6] == "X":
        print("You Won The Game")
        break

    elif user[1] == user[4] == user[7] == "X":
        print("You Won The Game")
        break

    elif user[2] == user[5] == user[8] == "X":
        print("You Won The Game")
        break

    elif user[0] == user[4] == user[8] == "X":
        print("You Won The Game")
        break

    elif user[2] == user[4] == user[6] == "X":
        print("You Won The Game")
        break

    # Computer board check

    if user[0] == user[1] == user[2] == "O":
        print("Computer Won The Game")
        break

    elif user[3] == user[4] == user[5] == "O":
        print("Computer Won The Game")
        break

    elif user[6] == user[7] == user[8] == "O":
        print("Computer Won The Game")
        break

    elif user[0] == user[3] == user[6] == "O":
        print("Computer Won The Game")
        break

    elif user[1] == user[4] == user[7] == "O":
        print("Computer Won The Game")
        break

    elif user[2] == user[5] == user[8] == "O":
        print("Computer Won The Game")
        break

    elif user[0] == user[4] == user[8] == "O":
        print("Computer Won The Game")
        break

    elif user[2] == user[4] == user[6] == "O":
        print("Computer Won The Game")
        break

    random.shuffle(comp)  # Shuffles the numbers

print("\nThanks for playing")
