#!/usr/bin/python

# Two player connect4 over TCP
#
# Written for Python 2.6
#

import getopt, random, socket, sys, SocketServer

board_cols = 7
board_rows = 6

board = []

def usage():
    print("usage: connect4 -p port host")
    print("Options and arguments :")
    print("-p port\t: tcp port to listen on or connect to (1024-65535)")
    print("host\t: IP address to connect with")
    sys.exit(0)

def print_board(board):
    for row in board:
        print (" ".join(row))

def initialise_board(board):
    print("Initialising board....")
    for x in range(0,board_rows):
        board.append(["O"] * board_cols)

def valid_ip(ip):
    try:
        socket.inet_aton(ip)
        host_bytes = ip.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4
    except:
        return False

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:h')
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(100)

    for o, a in opts:
        if o == "-p":
            try:
                port = int(a)
            except:
                print("Please specify port as integer > 1023 and < 65536")
                usage()
                sys.exit(105)
            else:
                if port < 1024 or port > 65535:
                    print("Port should be between 1024 and 65535")
                    usage()
                    sys.exit(110)
        elif o == "-h":
            usage()
        else:
            assert False, "unhandled option"

    if len(args) == 0:
        print("Please specify IP address to play")
        usage()
        sys.exit(120)
    elif len(args) > 1:
        print("Extra arguments passed")
        usage()
        sys.exit(130)
    else:
        ip = ''.join(args)
        if not valid_ip(ip):
            print("Invalid IP address " + ip)
            usage()
            sys.exit(140)




    initialise_board(board)
    print_board(board)



# Main

if __name__ == "__main__":
    main()
