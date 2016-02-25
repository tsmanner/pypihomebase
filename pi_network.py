import socket

my_ip = str(socket.gethostbyname(socket.gethostname()))
base_ip = my_ip[:my_ip.rfind('.')+1]

for i in range(0, 255):
    test_ip = base_ip + str(i)
    print(test_ip, end=' ')
    try:
        print(socket.gethostbyaddr(test_ip)[0])
    except socket.herror:
        print("None")
