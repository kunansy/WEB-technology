import random

R = 5


def f(x: float, y: float, r: float) -> bool:
    if x * y < 0:
        return False

    if x >= 0:
        return x**2 + y**2 <= r**2
    return y >= -r - x
    

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
