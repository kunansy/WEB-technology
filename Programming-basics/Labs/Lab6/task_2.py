# ЛР 4 to a file
import random
from pathlib import Path
from typing import List

# skip the values in this range
WRONG_RANGE_START = -5
WRONG_RANGE_STOP = -3

# values will be generated in this range
VALUE_START = -5
VALUE_STOP = 5

input_file = Path("task_2_input.txt")
output_file = Path("task_2_output.txt")


def number_of_min_element(sample: List[float]) -> int:
    """ Get number of minimal element by abs.

    :param sample: list of float, sample to work with.
    :return: int, number of minimal element by ads.
    """
    minimal = number = None
    for num, element in enumerate(sample, 1):
        if minimal is None or abs(element) < minimal:
            minimal = abs(element)
            number = num
    return number


def index_of_first_negative(sample: List[float]) -> int:
    """ Get the index of the first
    negative element in sample.

    Return -1 if there is no negative number.

    :param sample: list of float, sample to work with.
    :return: int, index if the first negative element
    if there is or -1 if there is no negative items.
    """
    for index, item in enumerate(sample):
        if item < 0:
            return index
    return -1


def sum_of_abs(sample: List[float]) -> float:
    """
    :param sample: list of float, sample to work with.
    :return: float, sum of elements by abs.
    """
    return sum(
        abs(item) for item in sample
    )


def change_sample(sample: List[float]) -> List[float]:
    """ Skip all elements which are in wrong range.
    Add zeroes to the end of the sample, which
    count is equal to the count of removed items.

    :param sample: list of float, sample to work with.
    :return: list of float, changed sample.
    """
    res = []
    wrong_items_count = 0
    for item in sample:
        if WRONG_RANGE_START <= item <= WRONG_RANGE_STOP:
            wrong_items_count += 1
        else:
            res += [item]
    res += [0] * wrong_items_count
    return res


def str_sample(sample: List[float],
               separator: str = ', ') -> str:
    """ Convert the sample to str, limit
    the count of signs after dot with 1.

    :param sample: list of float, sample to convert.
    :param separator: str, with this symbol values
    of the sample will be joined.
    :return: str.
    """
    res = separator.join(
        f"{item:.1f}" for item in sample
    )
    return res


def main() -> None:
    try:
        with input_file.open() as f:
            angle = next(f)
        length = int(angle)
        assert length <= 30
    except FileNotFoundError:
        print("File with input data not found",
              file=output_file.open('w'))
        return
    except ValueError:
        print("Wrong input", file=output_file.open('w'))
        return
    except AssertionError:
        print("List length is expected to be less than 30",
              file=output_file.open('w'))
        return

    sample = [
        random.uniform(-5, 5)
        for _ in range(length)
    ]

    num_of_min = number_of_min_element(sample)
    first_negative_index = index_of_first_negative(sample)
    if first_negative_index is -1:
        sum_of_abs_ = "oops, there is no negative element"
    else:
        sum_of_abs_ = sum_of_abs(sample[first_negative_index + 1:])
        sum_of_abs_ = f"{sum_of_abs_:.1f}"

    changed_sample = change_sample(sample)

    with output_file.open('w', encoding='utf-8') as f:
        f.write(f"Length: {length}\n")
        f.write(f"Sample: \n{str_sample(sample)}\n")

        f.write(f"Number of minimal by abs element: {num_of_min}\n")
        f.write(f"Sum of abs of values after the first negative: {sum_of_abs_}\n")
        f.write(f"Changed sample: \n{str_sample(changed_sample)}")


if __name__ == '__main__':
    main()
