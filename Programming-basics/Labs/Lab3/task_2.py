from Labs.Lab2.task_2 import f
import random

R = 5


def write_head() -> None:
    print("+--------+--------+--------+")
    print("|   X    |    Y   | Result |")
    print("+--------+--------+--------|")


def write_end() -> None:
    print("+--------+--------+--------+")


def write(x: float, y: float, result: bool) -> None:
    result = "yes" if result else "no"

    out_x = f"{x:.1f}".ljust(5).rjust(8)
    out_y = f"{y:.1f}".ljust(5).rjust(8)
    out_res = f"{result}".ljust(5).rjust(8)
    print(f"|{out_x}|{out_y}|{out_res}|")


def main() -> None:
    write_head()

    for _ in range(10):
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        result = f(x, y, R)
        write(x, y, result)
    write_end()


if __name__ == '__main__':
    main()
