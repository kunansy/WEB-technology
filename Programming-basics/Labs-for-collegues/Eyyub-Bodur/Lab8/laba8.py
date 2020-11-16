import matplotlib.pyplot as plt
import csv


def data(filename):
    with open(filename, encoding='utf-8') as d:
        reader = csv.reader(d)
        data = list(reader)

        labels = data[0]
        percents = []
        for percent in data[1]:
            percents.append(float(percent))
        return labels, percents


def graphic(plot, data, labels, explode, radius=1, center=(0, 0)):
    plot.pie(data, labels=labels, autopct='%1.1f%%', explode=explode, radius=radius, shadow=True, center=center)
    plot.legend(loc='lower right', labels=labels, title="Страны", shadow=True)


l1, d1 = data('data2014.csv')
l2, d2 = data('data2019.csv')

fig, (rating_2014, rating_2019) = plt.subplots(1, 2)
fig.canvas.set_window_title('ТОП-10 стран по добыче нефти в 2014-2019 годах')

# рисуем первую диаграмму
graphic(rating_2014, d1, l1, (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0))
rating_2014.set_title('Добыча нефти в 2014')

# рисуем вторую диаграмму
graphic(rating_2019, d2, l2, (0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0))
rating_2019.set_title('Добыча нефти в 2019')

# показываем график
plt.show()
