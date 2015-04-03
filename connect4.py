#!/usr/bin/python

# Two player connect4 over TCP
#
# Written for Python 2.6
#

import getopt, random, socket, sys, SocketServer

board_cols = 7
board_rows = 6

board = []

def print_board(board):
    for row in board:
        print (" ".join(row))

def initialise_board(board):
    print("Initialising board....")
    for x in range(0,board_rows):
        board.append(["O"] * board_cols)

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:')
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(100)

    for o, a in opts:
        if o == "-p":
            try:
                port = int(a)
            except:
                print("Please specify port as integer > 1024 and < 65536")
                sys.exit(105)
            else:
                if port < 1025 or port > 65535:
                    print("Port should be between 1024 and 65535")
                    sys.exit(110)
        else:
            assert False, "unhandled option"

    print(opts)
    print(args)
    print(port)

    initialise_board(board)
    print_board(board)



# Main

if __name__ == "__main__":
    main()
