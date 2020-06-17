print(" Welcome To Tic Tac Toe Game\n")

user = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
comp = [0, 1, 2, 3, 4, 5, 6, 7, 8]
x = y = 0

'''

Game Logic Explanation

This game can be played by two members

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
    # User 1 input with error check
    try:
        x = int(input("<User 1 (X)> Enter (1-9) numbers: "))
    except ValueError:
        print("Enter only numbers")

    if x not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        print("Enter numbers 1-9")
        continue

    try:
        # Removing the number entered by user 1
        comp.remove(x-1)

    except ValueError:
        print("Enter number of empty box")
        continue

    user[x-1] = "X"
    board()

    # Tie

    if not comp:
        print("Tie")
        break

    # User 2 input with error check

    try:
        y = int(input("<User 2 (O)> Enter (1-9) numbers: "))
    except ValueError:
        print("Enter only numbers")

    if y not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        print("Enter numbers 1-9")
        continue

    try:
        # Removing the number entered by user 2
        comp.remove(y-1)

    except ValueError:
        print("Enter number of empty box")
        continue

    user[y-1] = "O"
    board()

    # User 1 board check

    if user[0] == user[1] == user[2] == "X":
        print("User 1 Won The Game")
        break

    elif user[3] == user[4] == user[5] == "X":
        print("User 1 Won The Game")
        break

    elif user[6] == user[7] == user[8] == "X":
        print("User 1 Won The Game")
        break

    elif user[0] == user[3] == user[6] == "X":
        print("User 1 Won The Game")
        break

    elif user[1] == user[4] == user[7] == "X":
        print("User 1 Won The Game")
        break

    elif user[2] == user[5] == user[8] == "X":
        print("User 1 Won The Game")
        break

    elif user[0] == user[4] == user[8] == "X":
        print("User 1 Won The Game")
        break

    elif user[2] == user[4] == user[6] == "X":
        print("User 1 Won The Game")
        break

    # User 2 board check

    if user[0] == user[1] == user[2] == "O":
        print("User 2 Won The Game")
        break

    elif user[3] == user[4] == user[5] == "O":
        print("User 2 Won The Game")
        break

    elif user[6] == user[7] == user[8] == "O":
        print("User 2 Won The Game")
        break

    elif user[0] == user[3] == user[6] == "O":
        print("User 2 Won The Game")
        break

    elif user[1] == user[4] == user[7] == "O":
        print("User 2 Won The Game")
        break

    elif user[2] == user[5] == user[8] == "O":
        print("User 2 Won The Game")
        break

    elif user[0] == user[4] == user[8] == "O":
        print("User 2 Won The Game")
        break

    elif user[2] == user[4] == user[6] == "O":
        print("User 2 Won The Game")
        break


print("\nThanks for playing")
