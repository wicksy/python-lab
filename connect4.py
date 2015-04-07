#!/usr/bin/python

# Two player connect4 over TCP
#
# Written for Python 2.6
#

import getopt, os, random, socket, sys, SocketServer

board_cols = 7
board_rows = 6

board = []
server = 0
server_ip = "0.0.0.0"

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print("Unexpected error creating socket")
    usage()
    sys.exit(100)
else:
    pass

class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print "%s wrote:" % self.client_address[0]
        print self.data
        # just send back the same data, but upper-cased
        self.request.send(self.data.upper())

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

def tryconnect(ip,port,sock):
    print("Attempting to connect to " + str(ip) + " on port " + str(port))
    try:
        sock.connect((ip, port))
    except:
        print("Host does not appear to be listening on that port")
        return False
    else:
        return True

def startserver(ip,port,sock, server):
    try:
        server = SocketServer.TCPServer((ip, port), MyTCPHandler)
    except:
        print("Unexpected error starting server on port " + str(port))
        sys.exit(105)
    else:
        try:
            server.serve_forever()
        except:
            print("Server ended unexpectedly")
            sys.exit(106)

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:h')
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(110)

    for o, a in opts:
        if o == "-p":
            try:
                port = int(a)
            except:
                print("Please specify port as integer > 1023 and < 65536")
                usage()
                sys.exit(120)
            else:
                if port < 1024 or port > 65535:
                    print("Port should be between 1024 and 65535")
                    usage()
                    sys.exit(130)
        elif o == "-h":
            usage()
        else:
            assert False, "unhandled option"

    if len(args) == 0:
        print("Please specify IP address to play")
        usage()
        sys.exit(140)
    elif len(args) > 1:
        print("Extra arguments passed")
        usage()
        sys.exit(150)
    else:
        ip = ''.join(args)
        if not valid_ip(ip):
            print("Invalid IP address " + ip)
            usage()
            sys.exit(160)

    if not pingtest(ip):
        sys.exit(170)
    
    if tryconnect(ip,port,sock):
        print("Acting as client")
        sock.send("READY")
    else:
        print("Acting as server")
        startserver(server_ip,port,sock,socket)


    initialise_board(board)
    print_board(board)

# Main

if __name__ == "__main__":
    main()






#HOST, PORT = "localhost", 9999
#data = " ".join(sys.argv[1:])

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#sock.connect((HOST, PORT))
#sock.send(data + "\n")

#received = sock.recv(1024)
#sock.close()

#print "Sent:     %s" % data
#print "Received: %s" % received




    # Create the server, binding to localhost on port 9999
    #server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    #server.serve_forever()
