#Listing 1.5 integer convertion
#!/usr/bin/env python
# Python Network Programming Cookbook,Second Edition -- Chapter - 1


import socket

def integer_convertion():

    data= 1234
    cov32 = socket.ntohl(data) #converts from the network byte order to host byte order in a long format

    cov16 = socket.htons(data) #convert from host byte to network byte order in short format
    print("--------32-bit-------")
    print(f"Original: {data}  Long Host and Network byte order => {cov32} ")

    print("--------16-bit-------")
    print(f"Original: {data}  Short Host and Network byte order => {cov16} ")



integer_convertion()

#examples:
uint32_t_network_order = 0x12345678 #Data in network byte order
uint32_t_host_order = socket.ntohl(uint32_t_network_order)
print('Case1: -----------------------------')
print(f"32-bit: Network order => {uint32_t_network_order} to Host order => {uint32_t_host_order}")

print('Case2 ------------------------------')
uint16_t_host_order = 80; # Port number
uint16_t_network_order = socket.htons(uint16_t_host_order);
print(f"16-bit: Host order => {uint16_t_host_order} to network order => {uint16_t_network_order}")








#help(socket.ntohl) #Convert a 32-bit integer from network to host byte order. h represent host, l represent long
#help(socket.htons) #Convert a 16-bit unsigned integer from host to network byte order. n represent network, s represent short