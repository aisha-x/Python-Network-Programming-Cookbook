#Listing 1.7 socket_errors
#!/usr/bin/env python
#Python Network Programming Cookbook, Second Edition -- Chapter -
'''
Argument parsing is used in programming to allow scripts or applications to accept command-line arguments as input,
enabling users to configure or modify the behavior of a script without needing to edit the code.

--host: Specifies the argument name.
action='store': The value provided by the user will be stored.
dest='host': Assigns the argument's value to the variable host.
required=False: Indicates that the argument is optional.
'''

import socket
import sys
import argparse

def main():
    #set up an argument parsing, and description of the script purpose
    parser = argparse.ArgumentParser(description='Socket Error example')

    #start defining args, the script define three args
    parser.add_argument('--host', action='store', dest='host', required=False)
    parser.add_argument('--port', action='store', dest='port', type=int, required=False)
    parser.add_argument('--file', action='store', dest='file', required=False)

    #The parse_args method processes the arguments passed from the command line:
    given_arg = parser.parse_args()
    host = given_arg.host
    port = given_arg.port
    filename = given_arg.file

    #First try-except --Creating socket
    try:
        #ip4 addr, tcp connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print(f"Error 1: in Creating Socket: {msg}")
        sys.exit(1)

    #Second try-except --Connect to given Host, Port
    try:
        s.connect((host, port))
    except socket.gaierror as msg:
        print(f"Error 2: Address-related error connection to server {msg}")
        sys.exit(1)
    except socket.error as msg:
        print(f"Error 2: Connection Error {msg}")

    #Third try-except --Sending Data
    try:
        data = "GET %s HTTP/1.0\r\n\r\n" % filename
        s.sendall(data.encode("utf-8"))
    except socket.error as msg:
        print(f"Error 3: Error in sending data {msg}")
        sys.exit(1)
    while 1:
        #Fourth try-except --Waiting to receive data from remote host
        try:
            buf = s.recv(2048)
        except socket.error as msg:
            print("Error 4: Error in receiving data %s " % msg)
            sys.exit(1)
        if not len(buf):
            break
        #wait the received data
        sys.stdout.write(buf.decode("utf-8"))


if __name__ == '__main__':
    main()


'''
used in terminal.
use case example:
python Socket-error-handling.py --host=google.com --port=80 --file=Socket-error-handling.py
'''
