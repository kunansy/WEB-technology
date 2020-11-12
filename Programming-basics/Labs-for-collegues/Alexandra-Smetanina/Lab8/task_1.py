#!/usr/bin/env python3
import csv
from pathlib import Path

import matplotlib.pyplot as plt

PL_OLD_PATH = Path('pl_2010.csv')
PL_NEW_PATH = Path('pl_2020.csv')


def get_data(path: Path):
    with path.open(encoding='utf-8', newline='') as f:
        reader = csv.reader(f)

        headers = next(reader)
        data = next(reader)
        data = [float(value) for value in data]

        return data, headers


class Colors:
    grey = '#999999'
    green = '#00ff00'
    orange = '#ffa000'
    blue = '#000099'
    red = 'red'
    yellow = 'yellow'


def main(r_old_pl_rating: float = 1,
         r_new_pl_rating: float = 1,
         old_pl_rating_center=(0, 0),
         new_pl_rating_center=(0, 0)) -> None:
    pl_old_rating, pl_old_names = get_data(PL_OLD_PATH)
    pl_new_rating, pl_new_names = get_data(PL_NEW_PATH)

    fig, (pl_rating_2010, pl_rating_2020) = plt.subplots(1, 2)
    fig.canvas.set_window_title('ЯП в 2010-2020 годах')

    colors = (
        Colors.orange, Colors.grey, Colors.blue, Colors.yellow, Colors.red
    )
    pl_rating_2010.pie(
        pl_old_rating,
        labels=pl_old_names,
        colors=colors,
        autopct='%1.1f%%',
        radius=r_old_pl_rating,
        shadow=True,
        center=old_pl_rating_center
    )
    pl_rating_2010.legend(
        loc='lower left',
        labels=pl_old_names,
        title='Языки',
        shadow=True
    )
    pl_rating_2010.set_title('Рейтинг ЯП в 2010')

    colors = (
        Colors.grey, Colors.green, Colors.orange, Colors.blue, Colors.red
    )
    pl_rating_2020.pie(
        pl_new_rating,
        labels=pl_new_names,
        colors=colors,
        explode=(0, 0.1, 0, 0, 0),
        autopct='%1.1f%%',
        radius=r_new_pl_rating,
        shadow=True,
        center=new_pl_rating_center
    )
    pl_rating_2020.legend(
        loc='lower right',
        labels=pl_new_names,
        title='Языки',
        shadow=True
    )
    pl_rating_2020.set_title('Рейтинг ЯП в 2020')

    plt.show()


if __name__ == "__main__":
    main()
