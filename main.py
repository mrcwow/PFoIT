import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def f_1(y):
    return 1.4 + 0.12 * math.cos(3 * y)


def n_1_function(y, w):
    return f_1(y) * (1 - (0.35 * 1e14 / w) ** 2)


def calculate_sin_gamma(sin_alpha, n_1, n_2, direction):
    sin_gamma = n_1 * sin_alpha / n_2
    if sin_gamma > 1:
        direction *= -1
        sin_gamma = sin_alpha
    return sin_gamma, direction


def calculate_x(x_prev, dx):
    return x_prev + dx


def processing(L, D, n_0, alpha, w):
    sin_alpha = math.sin(alpha)
    n_1 = [n_1_function(0, w)]
    direction = 1
    sin_gamma, direction = calculate_sin_gamma(sin_alpha, n_0, n_1[0], direction)
    y = [0]
    step_line = 0.0001
    y.append(y[0] + sin_gamma * step_line)
    x = [0]
    i = 1
    x.append(step_line ** 2 - y[1] ** 2)
    sin_alpha = math.sin(math.radians(90) - math.asin(sin_gamma))
    # print(math.radians(90), math.asin(sin_gamma), sin_gamma)
    new_y = 0
    new_x = 0
    while new_x <= L:
        n_1.append(n_1_function(y[i], w))
        sin_gamma, direction = calculate_sin_gamma(sin_alpha, n_1[i-1], n_1[i], direction)
        dx = sin_gamma * step_line
        new_x = calculate_x(x[i], dx)
        x.append(new_x)
        dy = math.sqrt(step_line ** 2 - dx ** 2)
        new_y = y[i] + direction * dy
        if abs(new_y) > D:
            direction *= -1
            new_y = y[i] + direction * dy
        y.append(new_y)
        sin_alpha = sin_gamma
        i += 1
    alpha = math.degrees(math.atan((y[len(y) - 1] - y[len(y) - 2]) / (x[len(x) - 1] - x[len(x) - 2])))
    return x, y, alpha


L = 18
D = 0.8
n_2 = 1
n_0 = f_1(0)
alpha = math.radians(40)
w_red = 3.3 * 1e14
w_purple = 6.5 * 1e14
x1, y1, angle1 = processing(L, D, n_0, alpha, w_red)
x2, y2, angle2 = processing(L, D, n_0, alpha, w_purple)
beta = abs(angle1 - angle2)
print(beta)
file = open('./result.txt', 'w')
file.write(str(beta))
file.close()
fig, ax = plt.subplots()
ax.plot(x1, y1, color="red")
ax.plot(x2, y2, color="purple")
ax.add_patch(Rectangle((0, -D), L, 2 * D, fill=False))
fig.savefig('graphics.jpeg')

