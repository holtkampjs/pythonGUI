#!/usr/bin/env python3

import math
import socket
import numpy as np

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
x = 0
y = 0
angle = 0
sensors = 0b000000
sensor_data = np.array([])

for i in range(91):
    sensor_data = np.append(sensor_data, [64.5])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        start = conn.recv(1).decode('utf-8')
        print(start)

        if start == 'c':
            while True:
                for i in range(91):
                    temp = input(i * 2 + ' degrees: ')
                    if not temp == "":
                        sensor_data[i] = temp
                    else:
                        sensor_data[i] = 64.5
                cybot_out = x + '\n' + y + '\n' + angle + '\n' + sensors + '\n'
                for reading in sensor_data:
                    cybot_out += reading + '\n'
                cybot_out += ';'

                encoded = cybot_out.encode('utf-8')

                # This
                for b in encoded:
                    s.send(b)
                # or this
                # s.sendall(encoded)

                cybot_in_dir = s.recv(1).decode('utf-8')
                cybot_in_val = ""
                while True:
                    next = s.recv(1)
                    if next == 'g':
                        break
                    cybot_in_val += next

                cybot_in_val = cybot_in_val.decode('utf-8')

                if cybot_in_dir == 'a':
                    angle += cybot_in_val % 360
                elif cybot_in_dir == 'd':
                    angle -= cybot_in_val % 360
                elif cybot_in_dir == 'w':
                    x += cybot_in_val * math.cos(angle)
                    y += cybot_in_val * math.sin(angle)
                elif cybot_in_dir == 's':
                    x -= cybot_in_val * math.cos(angle)
                    y -= cybot_in_val * math.sin(angle)
