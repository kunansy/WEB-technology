import sys


def f(x: float, y: float, r: float) -> bool:
    if x * y < 0:
        return False

    if x >= 0:
        return x**2 + y**2 <= r**2
    return y >= -r - x


def main() -> str:
    try:
        x, y, r = map(float, input("Enter the point (x, y) and R: ").split())
    except ValueError:
        print("Wrong input", file=sys.stderr)
        exit(-1)

    if f(x, y, r):
        return "Попадает"
    return "Не попадает"


if __name__ == '__main__':
    print(main())
