import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
def get_data(file):
    with open(file, encoding='utf-8') as f:
        reader = csv.reader(f)
        vals = next(reader)
        res = []

        for val in vals:
            res.append(float(val))
        return res
def drow():
    try:
        vals = get_data('data.csv')
    except FileNotFoundError:
        print("Файл со входными данными не найден")
        exit(-1)
    fig = plt.figure()
    ax = Axes3D(fig)
    fig.canvas.set_window_title('Прибыль, $')
    achx = [0, 2, 4, 6, 0, 2, 4, 6, 0, 2, 4, 6]
    achy = [0, 0, 0, 0, 2, 2, 2, 2, 4, 4, 4, 4]
    achz = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    x = y = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ax.bar3d(achx, achy, achz, x, y, vals, shade=True)
    ax.set_title("Прибыль, $")
    ax.text2D(0.23, 0.92, "Прибыль, $", transform=ax.transAxes)
    ax.set_xlabel("Сезон")
    ax.set_zlabel("Доход")
    ax.set_ylabel("Временной период")
    xtics = [0.5 + i * 2 for i in range(4)]
    xv = ["Лето", "Весна", "Осень", "Зима"]
    plt.xticks(xtics, xv)
    ytics = [0.5 + i * 2 for i in range(3)]
    revenue = ["1990~2000", "2000~2013", "2013~настоящее время"]
    plt.yticks(ytics, revenue)
    rec = plt.Rectangle((0, 0), 1, 1)
    ax.legend([rec, rec, rec], revenue)
    plt.show()

drow()
