# ЛР 1 to a file
import math
from pathlib import Path

input_file = Path("task_1_input.txt")
output_file = Path("task_1_output.txt")


def main():
    try:
        with input_file.open() as inp:
            angle = next(inp)
        angle_in_gradus = float(angle)
    except FileNotFoundError:
        print("File with input data not found",
              file=output_file.open('w'))
        return
    except ValueError:
        print("Wrong angle given, numerical value was expected",
              file=output_file.open('w'))
        return
    angle_in_rads = math.radians(angle_in_gradus)

    try:
        z1 = ((1 - 2 * math.sin(angle_in_rads)**2) /
              (1 + math.sin(angle_in_rads * 2)))
    except ZeroDivisionError:
        print("It's impossible to calculate the value, division by zero",
              file=output_file.open('w'))
    else:
        print(f"z1 = {z1:.10f}", file=output_file.open('w'))

    try:
        z2 = ((1 - math.tan(angle_in_rads)) /
              (1 + math.tan(angle_in_rads)))
    except ZeroDivisionError:
        print("It's impossible to calculate the value, division by zero",
              file=output_file.open('a'))
    else:
        print(f"z2 = {z2:.10f}", file=output_file.open('a'))


if __name__ == "__main__":
    main()
