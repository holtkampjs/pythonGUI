import socket as sk
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy.core.defchararray import array


class Graph:
    xpath, ypath = [0], [0]
    xtower, ytower, xshort, yshort, xhole, yhole, xwall, ywall = [], [], [], [], [], [], [], []

    orientation: int = 0

    fig = plt.subplots()
    lnCybot, = plt.plot([], [], 'o--g', ms=10)
    lnTower, = plt.plot([], [], 'o', ms=20, mec='k', mfc='w')
    lnShort, = plt.plot([], [], 'ow', ms=2, mec='r', mfc='r')
    lnHole, = plt.plot([], [], 'sk', ms=5)
    lnWall, = plt.plot([], [], 'sw', ms=5)

    def __init__(self):
        self.display()

    def display(self):
        plt.title('CyBot View')

        ani = FuncAnimation(fig, )

        plt.show()

    # parse info and store relative data
    def parse_scan_data(self, scan: str):
        # break scan at '\n' delimiters
        info_list = scan.split('\n')
        self.xpath.append(self.xpath, info_list.pop(0))
        self.ypath.append(self.ypath, info_list.pop(0))
        # TODO Do more of this, then test on actual cybot
        self.lnCybot.set_data(self.xpath, self.ypath)

        self.orientation = info_list.pop(0)
        self.handle_upclose_sensors(info_list.pop(0))

        for i, reading in enumerate(info_list):
            if reading < 50:
                self.xtower.append(
                    self.xtower, reading * math.cos(self.orientation + 90 - i*2) + self.xpath[self.xpath.size - 1])
                self.ytower.append(
                    self.ytower, reading * math.sin(self.orientation + 90 - i*2) + self.ypath[self.ypath.size - 1])

    def handle_upclose_sensors(self, sensor_data: bytes):
        if sensor_data & 0b000001:
            for i in range(50):
                self.xshort.append(self.xshort,
                                   [18 * math.cos(self.orientation + 10 + i)] + self.xpath[self.xpath.size - 1])
                self.yshort.append(self.yshort,
                                   [18 * math.sin(self.orientation + 10 + i)] + self.ypath[self.ypath.size - 1])
        if sensor_data & 0b000010:
            for i in range(50):
                self.xshort.append(self.xshort,
                                   [18 * math.cos(self.orientation - 80 + i)] + self.xpath[self.xpath.size - 1])
                self.yshort.append(self.yshort,
                                   [18 * math.sin(self.orientation - 80 + i)] + self.ypath[self.ypath.size - 1])
        if sensor_data & 0b000100:
            for i in range(50):
                self.xhole.append(self.xhole,
                                  [18 * math.cos(self.orientation + 10 + i)] + self.xpath[self.xpath.size - 1])
                self.yhole.append(self.yhole,
                                  [18 * math.sin(self.orientation + 10 + i)] + self.ypath[self.ypath.size - 1])
        if sensor_data & 0b001000:
            for i in range(50):
                self.xhole.append(self.xhole,
                                  [18 * math.cos(self.orientation - 80 + i)] + self.xpath[self.xpath.size - 1])
                self.yhole.append(self.yhole,
                                  [18 * math.sin(self.orientation - 80 + i)] + self.ypath[self.ypath.size - 1])
        if sensor_data & 0b010000:
            for i in range(50):
                self.xwall.append(self.xwall,
                                  [18 * math.cos(self.orientation + 10 + i)] + self.xpath[self.xpath.size - 1])
                self.ywall.append(self.ywalll,
                                  [18 * math.sin(self.orientation + 10 + i)] + self.ypath[self.ypath.size - 1])
        if sensor_data & 0b100000:
            for i in range(50):
                self.xwall.append(self.xwall,
                                  [18 * math.cos(self.orientation - 80 + i)] + self.xpath[self.xpath.size - 1])
                self.ywall.append(self.ywall,
                                  [18 * math.sin(self.orientation - 80 + i)] + self.ypath[self.ypath.size - 1])


"""
The format we worked out for the data, listed in the order sent:
1. The x-coordinate of the robot's current position(start is considered the origin), in string form to short endian issues. The number string will be terminated by a newline.
2. The y-coordinate of the robot's current position, sent in string form and terminated by a newline.
3. The current angle the robot is facing(starts at zero). Increases when turning counter-clockwise. 0-359. Sent in string form and terminated by a newline.
4. Obstacle byte:
    0: bumpLeft: 1 if bumped, 0 otherwise.
    1: bumpRight: 1 if bumped, 0 otherwise.
    2: cliffLeft: 1 if cliff, 0 otherwise.
    3: cliffRight: 1 if cliff, 0 otherwise.
    4: tapeLeft: 1 if tape, 0 otherwise.
    5: tapeRight: 1 if tape, 0 otherwise.

After those four values, 91 distance values are sent, from 0-180 degrees in increments of 2. Sent in string form, each is newline-terminated.
I'm not crazy about the idea of using strings to send numbers. It's super wasteful, but it does short endian-ness issues.
"""

if __name__ == "__main__":
    # connect to CyBot
    HOST: str = input('IP Address: ')
    PORT: int = int(input('Port: '))
    s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    s.connect((HOST, PORT))

    print('Connected to ' + HOST + ':' + str(PORT))

    g = Graph()
    s.send(b'c')

    # read scan data
    while True:
        char = data = ""
        while not char == ';':
            char = s.recv(1)
            data += char.decode('utf-8')

        print(data)

        g.parse_scan_data(data)
        g.display()

        command = input("command> ")
        value = input("value> ")

        if command == "exit" or value == "exit":
            break
        # parse input (unnecesary if input correctly)
        bString = (command+value+'g').encode('utf-8')

        # this
        for b in bString:
            s.send(b)
        # or this
        # s.sendall(bString)

"""
71.189407
24.555244
1
000000
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
36.412885
36.410760
36.423507
36.413947
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.131663
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
16.469713
16.476087
16.430411
16.472900
16.473962
16.472900
16.470776
16.472900
16.432536
16.471838
16.476087
16.468651
16.477149
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.131663
65.042658
65.042658
65.042658
65.042658
65.042658
65.042658
65.087145
65.042658
;
"""
