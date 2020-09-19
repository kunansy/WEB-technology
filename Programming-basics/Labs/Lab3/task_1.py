import sys

from Labs.Lab2.task_1 import f


def write(start: float, stop: float, step: float) -> None:
    print("+--------+--------+")
    print("|   X    |    Y   |")
    print("+--------+--------+")

    x_current = start
    while x_current <= stop:
        out_x = f"{x_current:.1f}".ljust(5).rjust(8)
        out_y = f"{f(x_current):.1f}".ljust(5).rjust(8)

        print(f"|{out_x}|{out_y}|")

        x_current += step
    print("+--------+--------+")


def main() -> None:
    try:
        start, stop, step = map(float, input("Enter start, stop and step: ").split())
    except ValueError:
        print("Wrong input", file=sys.stderr)
        return
    write(start, stop, step)


if __name__ == '__main__':
    main()
