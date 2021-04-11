import matplotlib.pyplot as plt
import numpy as np
from pylab import *
from PIL import Image
from math import pi
from numpy import interp
from scipy.integrate import quad
from matplotlib import animation


def create_contour(image_name, *, level=[200]):
    image = Image.open(image_name).convert('L')
    im = array(image)
    image.close()
    
    contour_plot = contour(im, levels=level, colors='black', origin='image')
    contour_path = contour_plot.collections[0].get_paths()[0]
    x_table, y_table = contour_path.vertices[:, 0], contour_path.vertices[:, 1]
    time_table = np.linspace(0, 2*pi, len(x_table))
    
    x_table = x_table - min(x_table)
    y_table = y_table - min(y_table)
    x_table = x_table - max(x_table) / 2
    y_table = y_table - max(y_table) / 2
    
    return time_table, x_table, y_table


def f(t, time_table, x_table, y_table):
    return np.interp(t, time_table, x_table) + 1j*np.interp(t, time_table, y_table)


def coef_list(time_table, x_table, y_table, order=10):
    coef_list = []
    for n in range(-order, order+1):
        real_coef = quad(lambda t: np.real(f(t, time_table, x_table, y_table)
                                           * np.exp(-n*1j*t)), 0, 2*pi, limit=100, full_output=1)[0]/(2*pi)
        imag_coef = quad(lambda t: np.imag(f(t, time_table, x_table, y_table)
                                           * np.exp(-n*1j*t)), 0, 2*pi, limit=100, full_output=1)[0]/(2*pi)
        coef_list.append([real_coef, imag_coef])
    return np.array(coef_list)


def DFT(t, coef_list, order=10):
    kernel = np.array([np.exp(-n*1j*t) for n in range(-order, order+1)])
    series = np.sum((coef_list[:, 0]+1j*coef_list[:, 1]) * kernel[:])
    return np.real(series), np.imag(series)


def visualize(x_DFT, y_DFT, coef, order, space, fig_lim):
    fig, ax = plt.subplots()
    lim = 3*max(fig_lim)/2
    ax.set_xlim([-lim, lim])
    ax.set_ylim([-lim, lim])
    ax.set_aspect('equal')

    line = plt.plot([], [], 'k-', linewidth=2)[0]
    radius = [plt.plot([], [], 'r-', linewidth=0.5)[0]
              for _ in range(2 * order + 1)]
    circles = [plt.plot([], [], 'r-', linewidth=0.5)[0]
               for _ in range(2 * order + 1)]

    def update_c(c, t):
        new_c = []
        for i, j in enumerate(range(-order, order + 1)):
            theta = -j * t
            cos, sin = np.cos(theta), np.sin(theta)
            v = [cos * c[i][0] - sin * c[i][1], sin * c[i][0] + cos * c[i][1]]
            new_c.append(v)
        return np.array(new_c)

    def circle_sorting(order):
        idx = []
        for i in range(1, order+1):
            idx.extend([order+i, order-i])
        return idx

    def animate(i):
        line.set_data(x_DFT[:i], y_DFT[:i])
        r = [np.linalg.norm(coef[j]) for j in range(len(coef))]
        pos = coef[order]
        c = update_c(coef, i / len(space) * (2*pi))
        idx = circle_sorting(order)
        for j, rad, circle in zip(idx, radius, circles):
            new_pos = pos + c[j]
            rad.set_data([pos[0], new_pos[0]], [pos[1], new_pos[1]])
            theta = np.linspace(0, 2*pi, 50)
            x, y = r[j] * np.cos(theta) + pos[0], r[j] * np.sin(theta) + pos[1]
            circle.set_data(x, y)
            pos = new_pos

    plt.title('t.me/FourierTransformBot')
    ax.axis('off')
    ani = animation.FuncAnimation(fig, animate, frames=len(space), interval=50)
    return ani