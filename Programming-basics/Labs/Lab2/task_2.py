import sys


def f(x: float, y: float, r: float) -> bool:
    if x * y < 0:
        return False

    if x > 0:
        return x**2 + y**2 <= r**2
    return x**2 + y**2 >= r**2


def main() -> None:
    try:
        x, y, r = map(float, input("Enter the point: ").split())
    except ValueError:
        print("Wrong coords given", file=sys.stderr)
        exit(-1)
    print(f"Точка {x, y} ", end='')
    if f(x, y, r):
        print("попала")
    else:
        print("не попала")


if __name__ == '__main__':
    main()