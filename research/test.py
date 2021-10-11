import socket as sk


HOST: str = input('IP Address: ')
PORT: int = int(input('Port: '))
s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
s.connect((HOST, PORT))

print('Connected to ' + HOST + ':' + str(PORT))

data = s.recv(256)
print(repr(data))
