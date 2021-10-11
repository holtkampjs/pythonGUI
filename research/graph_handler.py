import numpy as np
import matplotlib.pyplot as plt


class Graph:
    xpath = np.array([0, 0, 25, 50])
    ypath = np.array([0, 50, 50, 60])
    xshort = np.array([30])
    yshort = np.array([15])
    xhole = np.array([-25, -30, -35])
    yhole = np.array([10, 12, 14])
    xwide = np.array([100, -50, -30, -65, 85, 40])
    ywide = np.array([-20, 110, 70, 110, 40, 85])
    xthin = np.array([70, 70, 100, 100])
    ythin = np.array([70, 100, 70, 100])

    def __init__(self):
        self.display()

    def display(this):
        plt.title('CyBot View')
        plt.plot(this.xpath, this.ypath, 'o--g', ms=10)
        plt.plot(this.xshort, this.yshort, 'o', ms=30, mec='k', mfc='w')
        plt.plot(this.xhole, this.yhole, 's-k', ms=20, linewidth=20)
        plt.plot(this.xwide, this.ywide, 'o', ms=20, mec='k', mfc='y')
        plt.plot(this.xthin, this.ythin, 'o', ms=15, mec='k', mfc='r')

        plt.show()


g = Graph()
