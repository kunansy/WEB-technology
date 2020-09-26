import sys


def f(x: float) -> float:
    if x <= -2:
        return -x - 2
    elif x <= -1:
        return (- x**2 - 2 * x)**0.5
    elif x <= 1:
        return 1.0
    elif x <= 2:
        return -2 * x + 3
    return -1.0
    

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
