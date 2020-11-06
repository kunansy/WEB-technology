#!/usr/bin/env python3
from pymorphy2 import MorphAnalyzer
from pathlib import Path
from typing import List


morph = MorphAnalyzer()
in_fios = Path('nom_fios.txt')


def inflect(word: str,
            case: str) -> str:
    word = morph.parse(word)[0]
    inflected_word = word.inflect({case})
    try:
        return inflected_word.word
    except AttributeError:
        return word


def inflect_fio(fio: str,
                case: str) -> str:
    surname, name, last_name = fio.split()

    surname = inflect(surname, case)
    name = inflect(name, case)
    last_name = inflect(last_name, case)

    return f"{surname} {name} {last_name}".title()


def get_fios(path: Path) -> List[str]:
    with path.open(encoding='utf-8') as f:
        fios = f.read().split('\n')
    return fios[:-1]


def main() -> None:
    fios = get_fios(in_fios)

    case = input("Enter the case you want: ")
    out_fios = Path(f"{case}_fios.txt")
    with out_fios.open('w', encoding='utf-8') as f:
        for fio in fios:
            fio = inflect_fio(fio, case)
            f.write(f"{fio}\n")


if __name__ == "__main__":
    main()
