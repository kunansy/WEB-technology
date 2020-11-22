import csv

import matplotlib.pyplot as plt


def getData(path):
    with open(path, encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)
        data = list(map(float, next(reader)))
        return data, headers


def writeDiagrams():
    d1, l1 = getData('f1.csv')
    d2, l2 = getData('f2.csv')

    x1 = range(1, len(d1) + 1)
    x2 = range(1, len(d2) + 1)
    fig, (gamers, games) = plt.subplots(1, 2)
    fig.canvas.set_window_title('Мобильные игры')

    gamers.bar(x1, d1)
    gamers.set_title('Кто играет в мобильные игры?')
    gamers.set_ylabel("Игроки, %")
    gamers.set_xlabel("Возраст игроков")
    gamers.set_xticks(x1)
    gamers.set_xticklabels(l1)
    gamers.legend()

    games.bar(x2, d2, color='red')
    games.set_title('Самые популярные игры')
    games.set_ylabel("Трафик, %")
    games.set_xlabel("Игры")
    games.set_xticks(x2)
    games.set_xticklabels(l2)
    games.legend()

    plt.show()


writeDiagrams()
