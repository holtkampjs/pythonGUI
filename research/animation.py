import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')


def init():
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    return ln,


def update(frame):
    tempx = input('Next x: ')
    tempy = input('Next y: ')

    if tempx == 'exit' or tempy == 'exit':
        sys.exit()
    elif tempx == 'change_lim':
        xmin = int(input('min x: '))
        xmax = int(input('max x: '))
        ymin = int(input('min y: '))
        ymax = int(input('max y: '))
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
    else:
        xdata.append(np.float64(tempx).item())
        ydata.append(np.float64(tempy).item())

    ln.set_data(xdata, ydata)
    return ln,


ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)
plt.show()
