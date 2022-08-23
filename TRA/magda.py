# fit data to exponential model

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import scipy.stats as stats


x_data = np.array([420, 500, 530, 540, 550, 560, 570, 590, 610, 630, 650])
y_data = [0.1, 0.4, 1.3, 1.9, 2.7, 4, 5.5, 11.9, 25, 52.6, 115.5]

def exp_func(x, a, b, c):
    return a * np.exp(b * x) + c


def exp_fit(x, y):
    popt, pcov = opt.curve_fit(exp_func, x, y, p0 = (1, 1e-6, 1))
    return popt, pcov

def exp_plot(x, y, popt, pcov):
    xl = np.linspace(x.min(), x.max(), 500)
    plt.plot(x, y, 'o', label='data')
    plt.plot(xl, exp_func(xl, *popt), '-', label='fit')
    plt.legend()
    plt.show()

exp_plot(x_data, y_data, *exp_fit(x_data, y_data))