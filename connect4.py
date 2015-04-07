#!/usr/bin/python

# Two player connect4 over TCP
#
# Written for Python 2.6
#

import getopt, os, random, socket, sys

board_cols = 7
board_rows = 6

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print("Unexpected error creating socket")
    usage()
    sys.exit(100)
else:
    pass

def usage():
    print("usage: connect4 -p port host")
    print("Options and arguments :")
    print("-p port\t: tcp port to listen on or connect to (1024-65535)")
    print("host\t: IP address to connect with")
    sys.exit(0)

def die(code, sock):
    try:
        sock.send("DIE")
        sock.close()
    except:
        pass
    print("Exit with code " + str(code))
    sys.exit(code)

def print_board(board):
    for row in board:
        print (" ".join(row))

def initialise_board(board):
    print("Initialising board....")
    for x in range(0, board_rows):
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

def pingtest(ip):
    print("Checking " + ip + " is alive")
    try:
        if os.system("ping -c 1 -W 2 " + ip + " > /dev/null 2>&1") == 0:
            print(ip + " appears to be alive")
            return True
        else:
            print(ip + " does not appear to be alive")
            return False
    except:
        print(ip + " does not appear to be alive")
        return False

def tryconnect(ip, port, sock):
    print("Attempting to connect to " + str(ip) + " on port " + str(port))
    try:
        sock.connect((ip, port))
    except:
        print("Host does not appear to be listening on that port")
        return False
    else:
        print("Connected OK")
        return True

def startserver(ip, port, sock):
    server_address = (ip, port)
    try:
        sock.bind(server_address)
        sock.listen(1)
        connection, client_address = sock.accept()
    except socket.error as err:
        print str(err)
        print("Socket error")
        die(110, sock)
    except:
        print("Unexpected error starting server on port " + str(port))
        die(120, sock)
    else:
        return connection

def serverread(sock, connection):
    try:
       data = connection.recv(1024)
       return data
    except:
       print("Server ended unexpectedly")
       die(130, sock)

def fill_column(board, col, mycolor):
    free = False
    col = int(col)
    for i in range(board_rows - 1, -1, -1):
        if board[i][col] == "O":
            board[i][col] = mycolor
            free = True
            break
    if free:
        return True
    else:
        return False

def check_win(board):

    win = False

    # Check horizontal win

    for i in range(board_rows - 1, -1, -1):
        red = yellow = 0
        for j in range(board_cols - 1, -1, -1):
            if board[i][j] == "R":
                yellow = 0
                red += 1
            elif board[i][j] == "Y":
                red = 0
                yellow += 1
            if red > 3 or yellow > 3:
                win = True

    # Check vertical win

    for i in range(board_cols - 1, -1, -1):
        red = yellow = 0
        for j in range(board_rows - 1, -1, -1):
            if board[j][i] == "R":
                yellow = 0
                red += 1
            elif board[j][i] == "Y":
                red = 0
                yellow += 1
            if red > 3 or yellow > 3:
                win = True

    # Check diagonal NW -> SE

    for i in range(board_rows - 4, -1, -1):
        for j in range(0, board_cols - 3, 1):
            red = yellow = 0
            for k in range(0,4):
                if board[i + k][j + k] == "R":
                    yellow = 0
                    red += 1
                elif board[i + k][j + k] == "Y":
                    red = 0
                    yellow += 1
                if red > 3 or yellow > 3:
                    win = True

    # Check diagonal NE -> SW

    for i in range(board_rows - 4, -1, -1):
        for j in range(board_cols - 1, board_cols - 5, -1):
            red = yellow = 0
            for k in range(0,4):
                if board[i + k][j - k] == "R":
                    yellow = 0
                    red += 1
                elif board[i + k][j - k] == "Y":
                    red = 0
                    yellow += 1
                if red > 3 or yellow > 3:
                    win = True

    return win

def main():

    board = []
    counters = 0

    server = 0
    server_ip = "0.0.0.0"
    ready = "READY"
    handshake = "NOT READY"
    mefirst = "ME FIRST"
    youfirst = "YOU FIRST"

    iamclient = False
    iamserver = False
    myturn = False

    playing = True

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:h')
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(140)

    for o, a in opts:
        if o == "-p":
            try:
                port = int(a)
            except:
                print("Please specify port as integer > 1023 and < 65536")
                usage()
                sys.exit(150)
            else:
                if port < 1024 or port > 65535:
                    print("Port should be between 1024 and 65535")
                    usage()
                    sys.exit(160)
        elif o == "-h":
            usage()
        else:
            assert False, "unhandled option"

    if len(args) == 0:
        print("Please specify IP address to play")
        usage()
        sys.exit(170)
    elif len(args) > 1:
        print("Extra arguments passed")
        usage()
        sys.exit(180)
    else:
        ip = ''.join(args)
        if not valid_ip(ip):
            print("Invalid IP address " + ip)
            usage()
            sys.exit(190)

    if not pingtest(ip):
        sys.exit(200)
    
    if tryconnect(ip, port, sock):
        print("Acting as client")
        iamclient = True
        sock.send(ready)
        handshake = sock.recv(1024)
        if handshake in mefirst + youfirst:
            print("Sever connected OK")
            if handshake == youfirst:
                print("I shall be going first")
                myturn = True
                mycolor = "R"
            else:
                print("Opponent will be going first")
                myturn = False
                mycolor = "Y"
        else:
            print("Unexpected response from server: " + handshake)
            die(210, sock)
    else:
        print("Acting as server")
        iamserver = True
        print("Waiting for client...")
        connection = startserver(server_ip, port, sock)
        handshake = serverread(sock, connection)
        if handshake == ready:
            print("Client connected OK")
            print("Picking who starts at random")
            if random.randint(0, 1000) % 2 == 0:
                print("I shall be going first")
                myturn = True
                mycolor = "R"
                connection.send(mefirst)
            else:
                print("Opponent will be going first")
                myturn = False
                mycolor = "Y"
                connection.send(youfirst)
        else:
            print("Unexpected response from client: " + handshake)
            die(220, connection)

    initialise_board(board)

# Main play loop

    while playing:
        print_board(board)
        if myturn: 
            colok = False
            while not colok:
                try:
                    mycol = input("Enter column: ")
                    x = abs(float(mycol))
                    y = int(x)
                    if x - y > 0:
                      print("Integers only. No floats")
                      colok = False
                    else:
                      mycol = int(mycol)
                      colok = True
                except (ValueError, SyntaxError, NameError, TypeError, AttributeError):
                    print("Please choose an integer")
                except KeyboardInterrupt:
                    print("")
                    print("Cancelling game")
                    die(230, sock)

                try:
                    if mycol < 0 or mycol >= board_cols:
                        print("Must be between 0 and " + str(board_cols-1))
                        colok = False
                except:
                    print("Invalid entry")
                    colok = False

                if colok:
                    gamedata = mycol
                    if iamserver:
                        try:
                            connection.send(str(mycol))
                        except:
                            print("Unexpected error sending response")
                            die(240, sock)
                    else:
                        try:
                            sock.send(str(mycol))
                        except:
                            print("Unexpected error sending response")
                            die(250, sock)
        else:
            print("Waiting for opponent turn...")
            if iamserver:
                try:
                    gamedata = serverread(sock, connection)
                except:
                    print("Unexpected error receiving response")
                    die(260, sock)
            else:
                try:
                    gamedata = sock.recv(1024)
                except:
                    print("Unexpected error receiving response")
                    die(270, sock)

        if gamedata == "DIE" or gamedata == "":
            print("Opponent sent kill message")
            die(280, sock)
        else:
            if mycolor == "R":
                theircolor = "Y"
            else:
                theircolor = "R"
            if myturn:
                fillcolor = mycolor
            else:
                fillcolor = theircolor
            if fill_column(board, gamedata, fillcolor):
                counters += 1
                if check_win(board):
                    print_board(board)
                    if myturn:
                        print("YOU WON!!!")
                        die(0,sock)
                    else:
                        print("YOU LOST!!!")
                        die(0,sock)
                if counters >= (board_cols * board_rows):
                    print("DRAW!!!")
                    die(0,sock)
                myturn = not myturn
            else:
                print("Column " + str(gamedata) + " is NOT free")

# Main

if __name__ == "__main__":
    main()

