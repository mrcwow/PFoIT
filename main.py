import matplotlib.pyplot as plt
import random
import copy


# во внешнем электроде
def checkin_outfig(x, y):
    return x * y + abs(x) ** 2 + abs(y) ** 2 < 16


# во внутреннем электроде
def checkin_infig(x, y):
    return x * y + 2 * abs(0.1 + x) ** 5/2 + abs(-0.1 + y) ** 5/2 <= 1


# размер поля
size = 150
# смещение
offset = 4.8
# соответствие масштабу
accordance = offset * 2 / size
# точность
eps = 10 ** -5
# поле
field_grid = [[random.uniform(0, 9) for i in range(0, size + 1)] for j in range(0, size + 1)]
for i in range(0, size + 1):
    for j in range(0, size + 1):
        # внешний
        if not checkin_outfig(j * accordance - offset, -i * accordance + offset):
            field_grid[i][j] = 0
        # внутренний
        elif checkin_infig(j * accordance - offset, -i * accordance + offset):
            field_grid[i][j] = 9

# метод
while True:
    field_grid_step_back = copy.deepcopy(field_grid)
    diff = 0
    for i in range(0, size + 1):
        for j in range(0, size + 1):
            if checkin_outfig(j * accordance - offset, -i * accordance + offset) and not checkin_infig(j * accordance - offset, -i * accordance + offset):
                field_grid[i][j] = 1 / 4 * (field_grid[i + 1][j] + field_grid[i - 1][j] + field_grid[i][j + 1] + field_grid[i][j - 1])
                diff = max(abs(field_grid[i][j] - field_grid_step_back[i][j]), diff)
    if diff < eps:
        break
# график
lines = [0, 1, 2, 3, 4, 5, 6, 7, 8]
fig, ax = plt.subplots()
ax.imshow(field_grid)
axlines = ax.contour(field_grid, levels=lines, colors="white")
ax.clabel(axlines, colors="white")
fig.savefig('graphics.jpeg')
# вычисление длины эквипотенциальной линии
arr_coor = axlines.allsegs[2][0]
length = 0
for i in range(-1, len(arr_coor) - 1):
    x1 = arr_coor[i][0]
    y1 = arr_coor[i][1]
    x2 = arr_coor[i + 1][0]
    y2 = arr_coor[i + 1][1]
    length += (((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5) * accordance
# запись в файл
file = open('./result.txt', 'w')
file.write(str(length))
file.close()