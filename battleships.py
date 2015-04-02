#!/usr/bin/python

# Battleships
#

from random import randint
from sys import exit

board_cols = 20
board_rows = 20

ship_specs = {
        'carrier'    : 6,
        'battleship' : 4,
        'destroyer'  : 3,
        'frigate'    : 2,
        'dinghy'     : 1
        }

ship_count = {
        'carrier'       : 1,
        'battleship'    : 1,
        'destroyer'     : 2,
        'frigate'       : 4,
        'dinghy'        : 6
        }

board = []
ship_pos = {}

def print_board(board):
    for row in board:
        print (" ".join(row))

def initialise_board(board):
    print("Initialising board....")
    for x in range(0,board_rows):
        board.append(["O"] * board_cols)

    ship_number = 0
    for ship in ship_count:
        print("Positioning " + ship + "(" + str(ship_count[ship]) + ")")
        for count in range(0,ship_count[ship]):
            position_ship(board,ship_specs[ship],ship_number)
            ship_number += 1

def check_free(board,row,col):
    if board[row][col] == "O":
        return True
    else:
        return False

def check_free_range_right(board,row,col,length):
    if col + length > board_cols:
        return False
    else:
        for i in range(col,col+length):
            if check_free(board,row,i):
                pass
            else:
                return False
        else:
            return True

def check_free_range_down(board,row,col,length):
    if row + length > board_cols:
        return False
    else:
        for i in range(row,row+length):
            if check_free(board,i,col):
                pass
            else:
                return False
        else:
            return True

def check_free_range_left(board,row,col,length):
    if col - length < 0:
        return False
    else:
        for i in range(col,col-length,-1):
            if check_free(board,row,i):
                pass
            else:
                return False
        else:
            return True

def check_free_range_up(board,row,col,length):
    if row - length < 0:
        return False
    else:
        for i in range(row,row-length,-1):
            if check_free(board,i,col):
                pass
            else:
                return False
        else:
            return True

def fill_ship_right(board,row,col,length,ship_number):
    for i in range(col,col+length):
        board[row][i] = "*"
        if i == col:
            ship_pos[ship_number] = [[row,i]]
        else:
            ship_pos[ship_number] += [[row,i]]

def fill_ship_down(board,row,col,length,ship_number):
    for i in range(row,row+length):
        board[i][col] = "*"
        if i == row:
            ship_pos[ship_number] = [[i,col]]
        else:
            ship_pos[ship_number] += [[i,col]]

def fill_ship_left(board,row,col,length,ship_number):
    for i in range(col,col-length,-1):
        board[row][i] = "*"
        if i == col:
            ship_pos[ship_number] = [[row,i]]
        else:
            ship_pos[ship_number] += [[row,i]]

def fill_ship_up(board,row,col,length,ship_number):
    for i in range(row,row-length,-1):
        board[i][col] = "*"
        if i == row:
            ship_pos[ship_number] = [[i,col]]
        else:
            ship_pos[ship_number] += [[i,col]]

def position_ship(board,length,ship_number):
    looking = True
    while looking:
        ship_row = randint(0,len(board) -1)
        ship_col = randint(0,len(board[0]) -1)
        if check_free_range_right(board,ship_row,ship_col,length):
            fill_ship_right(board,ship_row,ship_col,length,ship_number)
            looking = False
        elif check_free_range_down(board,ship_row,ship_col,length):
            fill_ship_down(board,ship_row,ship_col,length,ship_number)
            looking = False
        elif check_free_range_left(board,ship_row,ship_col,length):
            fill_ship_left(board,ship_row,ship_col,length,ship_number)
            looking = False
        elif check_free_range_up(board,ship_row,ship_col,length):
            fill_ship_up(board,ship_row,ship_col,length,ship_number)
            looking = False
        else:
            looking = True

def check_ship(board,row,col):
    if board[row][col] == "*":
        return True
    else:
        return False

def mark_spot(board,row,col):
    for each in ship_pos:
        for coords in ship_pos[each]:
            if coords == [row,col]:
                ship_pos[each].remove([row,col])

def check_ships(board):
    for each in ship_pos:
        if len(ship_pos[each]) == 0:
            del ship_pos[each]
            print("SHIP SUNK!")
            break

# Main

initialise_board(board)
playing = True
while playing:
    rowok = False
    while not rowok:
        try:
            myrow = input("Enter row guess: ")
            x = abs(myrow)
            y = int(x)
            if x - y > 0:
              print("Integers only. No floats")
              rowok = False
            else:
              myrow = int(myrow)
              rowok = True
        except (ValueError, SyntaxError, NameError, TypeError):
            print("Please choose an integer")
        except KeyboardInterrupt:
            print("")
            print("Cancelling game")
            exit(0)

        try:
            if myrow < 0 or myrow >= board_rows:
                print("Must be between 0 and " + str(board_rows-1))
                rowok = False
        except:
            print("Invalid entry")
            rowok = False

    colok = False
    while not colok:
        try:
            mycol = input("Enter col guess: ")
            x = abs(mycol)
            y = int(x)
            if x - y > 0:
              print("Integers only. No floats")
              colok = False
            else:
              mycol = int(mycol)
              colok = True
        except (ValueError, SyntaxError, NameError, TypeError):
            print("Please choose an integer")
        except KeyboardInterrupt:
            print("")
            print("Cancelling game")
            exit(0)

        try:
            if mycol < 0 or mycol >= board_cols:
                print("Must be between 0 and " + str(board_cols-1))
                colok = False
        except:
            print("Invalid entry")
            colok = False
        #else:
        #    if myrow == 0 and mycol == 0:
        #        print_board(board)
        #        print(ship_pos)

    if check_ship(board,myrow,mycol):
        board[myrow][mycol] = "X"
        mark_spot(board,myrow,mycol)
        print("HIT!!")
        check_ships(board)
        if len(ship_pos) == 0:
            print("Game over!")
            playing = False
    elif check_free(board,myrow,mycol):
        board[myrow][mycol] = "1"
        print("MISS!")
    else:
        print("Row " + str(myrow) + ", Col " + str(mycol) + " is already filled")
else:
  exit(0)
