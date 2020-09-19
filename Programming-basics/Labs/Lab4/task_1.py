import random
import sys
from typing import List, Tuple


def two_max_by_abs(sample: List[float]) -> Tuple[float, float]:
    first_max = second_max = abs(sample[0])
    for num in sample:
        if abs(num) > first_max:
            second_max, first_max = first_max, abs(num)
        elif abs(num) > second_max:
            second_max = abs(num)
    return first_max, second_max


def sum_of_less_than_one(sample: List[float]) -> float:
    return sum(
        num for num in sample
        if abs(num) < 1
    )


def zero_of_better_than(sample: List[float],
                        threshold_value: float) -> List[float]:
    return [
        num if abs(num) < threshold_value else 0
        for num in sample
    ]


def sort(sample: List[float]) -> List[float]:
    zeroes_count = sample.count(0)
    removed_zeroes = [
        num for num in sample
        if num is not 0
    ]
    return removed_zeroes + [0.0] * zeroes_count


def print_list(sample: List[float],
               changed_sample: List[float],
               threshold_value: float) -> None:
    print(f"Length: {len(sample)}")
    print(f"Threshold value: {threshold_value}")

    out_sample = (f"{num:.3f}" for num in sample)
    out_chg_sample = (f"{num:.3f}" for num in changed_sample)

    print(f"Beginning status: {', '.join(out_sample)}")
    print(f"Current status: {', '.join(out_chg_sample)}")

    first_max, second_max = two_max_by_abs(changed_sample)
    print(f"First max: {first_max:.3f}")
    print(f"Second max: {second_max:.3f}")
    print(f"Sum: {sum_of_less_than_one(sample):.3f}")


def main() -> None:
    try:
        length = int(input("Enter the list length: "))
        assert length <= 30
    except ValueError:
        print("Wrong input", file=sys.stderr)
        return
    except AssertionError:
        print("List length is expected to be less than 30",
              file=sys.stderr)
        return

    try:
        threshold_value = float(input("Enter the threshold value: "))
    except ValueError:
        print("Wrong input", file=sys.stderr)
        return

    sample = [
        random.uniform(-5, 5)
        for _ in range(length)
    ]
    changed_sample = zero_of_better_than(sample, threshold_value)
    changed_sample = sort(changed_sample)

    print_list(sample, changed_sample, threshold_value)


if __name__ == '__main__':
    main()
