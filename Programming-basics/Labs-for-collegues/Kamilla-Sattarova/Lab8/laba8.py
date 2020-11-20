import csv

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def get_data(file):
    with open(file) as f:
        reader = csv.reader(f)
        vals = []
        for val in next(reader):
            vals.append(float(val))
        return vals


def main():
    try:
        temperature = get_data('t.csv')
    except FileNotFoundError:
        print("Файл со входными данными не найден")
        exit(-1)

    # определяем полотно графика
    fig = plt.figure()
    ax = Axes3D(fig)
    fig.canvas.set_window_title('Температура воздуха')

    # положения столбцов
    anchor_x = [0, 2, 4, 6] * 3
    anchor_y = [0] * 4 + [2] * 4 + [4] * 4
    anchor_z = [0] * 12

    # значения столбцов
    x = [1] * 12
    y = [1] * 12

    colors = ['#ffc0cb'] * 4 + ['#00bfff'] * 4 + ['#8cff40'] * 4
    ax.bar3d(anchor_x, anchor_y, anchor_z, x, y, temperature, shade=True, color=colors)

    ax.set_title("Температура воздуха")
    ax.text2D(0.25, 0.95, "Температура воздуха", transform=ax.transAxes)
    ax.set_xlabel("Сезон")
    ax.set_zlabel("Температура")
    ax.set_ylabel("Годы")

    xtics = [0.5 + i * 2 for i in range(4)]
    xv = ["Лето", "Весна", "Осень", "Зима"]
    plt.xticks(xtics, xv)

    ytics = [0.5 + i * 2 for i in range(3)]
    yv = ["1887~1896", "1937~1946", "1987~1996"]
    plt.yticks(ytics, yv)

    pink_proxy = plt.Rectangle((0, 0), 1, 1, fc="#ffc0cb")
    blue_proxy = plt.Rectangle((0, 0), 1, 1, fc="#00bfff")
    green_proxy = plt.Rectangle((0, 0), 1, 1, fc="#8cff40")

    labels = [i + " годы" for i in yv]
    ax.legend([pink_proxy, blue_proxy, green_proxy], labels)
    plt.show()


main()
