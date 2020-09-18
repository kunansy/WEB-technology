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


def main() -> None:
    try:
        x = float(input("Enter x: "))
    except ValueError:
        print("Wrong value given", file=sys.stderr)
        exit(-1)
    print(f"f({x}) = {f(x)}")


if __name__ == '__main__':
    main()
