import matplotlib.pyplot as plt
import sys
from matplotlib import animation
import socket as sk
import math


"""
    Initialize the GUI for display with given size and axis labels
"""
fig = plt.figure()
ax1 = plt.axes(xlim=(-250, 250), ylim=(-250, 250))
line, = ax1.plot([], [], lw=2)
plt.xlabel('x')
plt.ylabel('y')


"""
    Initialize the different displays for the cybot, obatacles, and other 
    data read from the cybot to display
"""
plotlays, plotdis, plotms = [8], [
    "x:g", "ob", ",r", "sk", "sy", "*k", "og", "xr"], [3, 3, 2, 1, 1, 2, 10, 3]
lines = []
for index in range(8):
    lobj = ax1.plot([], [], plotdis[index], ms=plotms[index])[0]
    lines.append(lobj)


def init():
    for line in lines:
        line.set_data([], [])
    return lines


xcybot, ycybot, xtower, ytower, xshort, yshort, xhole, yhole, xwall, ywall, xdir, ydir, xloc, yloc, xgoal, ygoal = [
], [], [], [], [], [], [], [], [], [], [0], [0], [0], [0], [], []
orientation: int = 0

"""
    Function for parsing scan data received from the cybot via sockets
"""


def parse_scan_data(scan: str, scan_num):
    # break scan at '\n' delimiters
    info_list = scan.split('\n')

    # Read the x and y positions
    xcybot.append(float(info_list.pop(0)))
    ycybot.append(float(info_list.pop(0)))

    # Read the angle of the cybot to the axis it began on
    orientation = float(info_list.pop(0))

    # Handle the information from the upclose sensors on the cybot
    handle_upclose_sensors(info_list.pop(0), scan_num, orientation)

    # Set the marker for the direction the cybot is facing
    xdir[0] = int(xcybot[scan_num] + 45 * math.cos(to_rad(orientation)))
    ydir[0] = int(ycybot[scan_num] + 45 * math.sin(to_rad(orientation)))

    # Update the cybot's current location
    xloc[0] = xcybot[scan_num]
    yloc[0] = ycybot[scan_num]

    # Remove all points directly in front of the cybot for rescanning of the area
    newx, newy = [], []
    while xtower:
        tempx = xtower.pop()
        tempy = ytower.pop()

        delx = (xdir[0] + xloc[0]) / 2
        dely = (ydir[0] + yloc[0]) / 2

        magnitude = math.sqrt(
            math.pow(delx - tempx, 2) + math.pow(dely - tempy, 2))

        inRange: bool = abs(magnitude) < 25

        if not inRange:
            newx.append(tempx)
            newy.append(tempy)

    # Add back all points not in the direct scan region
    while newx:
        xtower.append(newx.pop())
        ytower.append(newy.pop())

    # Parse the angle/distance measurments to save the relevant points for display
    tempReading = 65
    tempReadingCount = 0
    for i, reading in enumerate(info_list):
        tempReadingCount += 1

        if reading == ';' or (float(reading) > tempReading + 2 or float(reading) < tempReading - 2):

            if tempReading < 45 and tempReading > 5 and tempReadingCount > 1:

                angle = to_rad(orientation + 90 - i * 2 + tempReadingCount)

                if tempReading < 50 and tempReading > 5:

                    inRange: bool = abs(90 - i * 2) < 30

                    print(tempReading)

                    # Calibration for locating the end zone pillars
                    if inRange and 66.384586 * math.pow(0.861401634, tempReadingCount) + 2.3 > tempReading and 66.384586 * math.pow(0.861401634, tempReadingCount) - 2.3 < tempReading:
                        xgoal.append(tempReading * math.cos(angle) +
                                     15 * math.cos(angle) + xloc[0])
                        ygoal.append(tempReading * math.sin(angle) +
                                     15 * math.sin(angle) + yloc[0])
                    else:
                        xtower.append(tempReading * math.cos(angle) +
                                      15 * math.cos(angle) + xloc[0])
                        ytower.append(tempReading * math.sin(angle) +
                                      15 * math.sin(angle) + yloc[0])

            if not reading == ';':
                tempReading = float(reading)
                tempReadingCount = 0

        if reading == ';':
            break

# Convert degrees to radians


def to_rad(angle: int):
    return angle * math.pi / 180

# Parses the upclose sensor data from the cybot


def handle_upclose_sensors(sensor_data: str, scan_num, dir):
    if sensor_data[0] == '1':
        for i in range(50):
            angle = to_rad(dir + 10 + i)
            xshort.append(18 * math.cos(angle) + xcybot[scan_num])
            yshort.append(18 * math.sin(angle) + ycybot[scan_num])
    if sensor_data[1] == '1':
        for i in range(50):
            angle = to_rad(dir - 80 + i)
            xshort.append(18 * math.cos(angle) + xcybot[scan_num])
            yshort.append(18 * math.sin(angle) + ycybot[scan_num])
    if sensor_data[2] == '1':
        for i in range(50):
            angle = to_rad(dir + 10 + i)
            xhole.append(18 * math.cos(angle) + xcybot[scan_num])
            yhole.append(18 * math.sin(angle) + ycybot[scan_num])
    if sensor_data[3] == '1':
        for i in range(50):
            angle = to_rad(dir - 80 + i)
            xhole.append(18 * math.cos(angle) + xcybot[scan_num])
            yhole.append(18 * math.sin(angle) + ycybot[scan_num])
    if sensor_data[4] == '1':
        for i in range(50):
            angle = to_rad(dir + 10 + i)
            xwall.append(18 * math.cos(angle) + xcybot[scan_num])
            ywall.append(18 * math.sin(angle) + ycybot[scan_num])
    if sensor_data[5] == '1':
        for i in range(50):
            angle = to_rad(dir - 80 + i)
            xwall.append(18 * math.cos(angle) + xcybot[scan_num])
            ywall.append(18 * math.sin(angle) + ycybot[scan_num])


"""
    Create the Websocket connection based by IP address and port number
"""
HOST: str = input('IP Address: ')
PORT: int = int(input('Port: '))
s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
s.connect((HOST, PORT))

print('Connected to ' + HOST + ':' + str(PORT))

# Send 'c' to signal connection to the cybot and to rescan
s.send(b'c')

"""
    Handles the communication back and forth between the cybot
    When given a command, it broadcasts to the cybot and waits for the response
    Then when the cybot responds, it compiles the response back into a string and passes it to the 
    parse_scan_data() function to update relevant data for display
    Finally it displays the visual of an overhead view of the cybot to the graph
"""


def animate(i):
    if int(i) != 0:
        command = input("command> ")
        if command == "exit":
            sys.exit()
        value = input("value> ")

        instruction = command + value + 'g'

        for step in range(len(instruction)):
            s.send(instruction[step].encode('ascii'))

    print('Executing commands...')

    char = data = ""
    while not char == ';':
        char = s.recv(1).decode('utf-8')
        if char == 'g':
            data = ""
        else:
            data += char

    parse_scan_data(data, i)

    xlist = [xcybot, xtower, xshort, xhole, xwall, xdir, xloc, xgoal]
    ylist = [ycybot, ytower, yshort, yhole, ywall, ydir, yloc, ygoal]

    # Sets the data to the graph by looping through each data set
    for lnum, line in enumerate(lines):
        # set data for each line separately.
        line.set_data(xlist[lnum], ylist[lnum])

    return lines


# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               interval=10, blit=True)

plt.show()
