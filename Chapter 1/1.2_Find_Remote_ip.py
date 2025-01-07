#Listing 1.2 show how to get remote machine's ip address
#!/usr/bin/env python
#Python Network Programming Cookbook, Second Edition -- Chapter - 1

import socket

def print_remote_ip_info():

    #remote_mach = 'www.pytgo.org' #to test the exception error
    remote_mach = 'www.python.org'
    try:
        print("The ip address of %s is : %s" % (remote_mach, socket.gethostbyname(remote_mach)))
    except socket.error as err_msg:
        print("%s : %s" % (remote_mach, err_msg))


if __name__ == '__main__':
    print_remote_ip_info()