import csv

import matplotlib.pyplot as plt


def get_data(file):
    with open(file, encoding='utf-8', newline='') as f:
        reader = csv.reader(f)

        labels = next(reader)
        res = []
        for value in next(reader):
            res.append(float(value))

        return res, labels


def write_pie(plot, data, labels, colors, radius=1, center=(0, 0)):
    plot.pie(data, labels=labels, colors=colors, autopct="%1.1f%%", radius=radius, center=center)
    plot.legend(loc="lower right", labels=labels, title="COVID-19")


yellow = "yellow"
orange = "#ffa000"
blue = "#000099"
green = "#00ff00"
grey = "#999999"
red = "red"


try:
    data, labels = get_data('covid-19-statistics.csv')
except FileNotFoundError:
    print("Файл с данными не существует!")
    exit(-1)

colors = orange, grey, blue, yellow, red

write_pie(plt, data, labels, colors)
plt.title("Количество заражённых COVID-19")
plt.show()
