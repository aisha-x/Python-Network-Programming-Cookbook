#Listing 1.1 show how to get our machine info
#!/usr/bin/env python
#Python Network Programming Cookbook,Second Edition -- Chapter - 1
import socket

def print_machine_info():

    #to get the host by name
    hostname = socket.gethostname()
    print("The name of the host machine: %s" %hostname)

    #to print the ip address of the host
    ip_address = socket.gethostbyname(hostname)
    print("Ip address: %s" %ip_address)

#you can call the function using this two ways
'''
if __name__ == '__main__':
    print_machine_info()'''

print_machine_info()

#to find information about a method in a module or any method was, use this method
help(socket.gethostbyname)