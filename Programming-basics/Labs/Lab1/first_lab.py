import math
import sys


def main():
    try:
        angle_in_gradus = float(input("Enter the angle in gradus: "))
    except ValueError:
        print("Wrong angle given, numeral value expected", file=sys.stderr)
        exit(-1)
    angle_in_rads = math.radians(angle_in_gradus)

    try:
        z1 = (1 - 2 * math.sin(angle_in_rads)**2) / (1 + math.sin(angle_in_rads * 2))
    except ZeroDivisionError:
        print("It's impossible to calculate the value, division by zero",
              file=sys.stderr)
    else:
        print(f"z1 = {z1}")

    try:
        z2 = (1 - math.tan(angle_in_rads)) / (1 + math.tan(angle_in_rads))
    except ZeroDivisionError:
        print("It's impossible to calculate the value, division by zero",
              file=sys.stderr)
    else:
        print(f"z2 = {z2}")


if __name__ == "__main__":
    main()
