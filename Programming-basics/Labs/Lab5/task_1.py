#!/usr/bin/env python3

import random
import sys
from typing import Any, List

RANGE_START = -1
RANGE_STOP = 1


class Matrix:
    def __init__(self,
                 rows: int,
                 cols: int = None) -> None:
        """ Create a matrix of rows*cols.
        If the number of cols is None (not given)
        create a square matrix rows*rows

        :param rows: int, count of rows.
        :param cols: int or None, count of columns.
        :return: None.
        """
        self.__rows, self.__cols = rows, cols or rows
        self.__matrix = Matrix.create_matrix(self.rows, self.cols)

    @property
    def rows(self) -> int:
        """
        :return: int, number of rows.
        """
        return self.__rows

    @property
    def cols(self) -> int:
        """
        :return: int, number of columns.
        """
        return self.__cols

    @classmethod
    def create_matrix(cls,
                      rows: int,
                      cols: int) -> Any:
        """ Create a matrix of rows*cols of random int.
        Values are in range [-RANGE; RANGE] (global const).

        :param rows: int, count of rows.
        :param cols: int, count of columns.
        :return: Matrix object.
        """
        matrix = [
            [random.randint(RANGE_START, RANGE_STOP) for _ in range(cols)]
            for _ in range(rows)
        ]
        return matrix

    def remove_zeroes_rows(self) -> None:
        """ Remove all rows, which elements are equal to 0.

        :return: None.
        """
        row_index = 0
        for _ in range(self.rows):
            if all(row == 0 for row in self[row_index]):
                del self[row_index]
                row_index -= 1
            row_index += 1
        self.__rows = len(self)

    def remove_zeroes_cols(self) -> None:
        """ Remove all columns, which elements are equal to 0.

        :return: None.
        """
        col_index = 0
        for _ in range(self.cols):
            if all(row[col_index] == 0 for row in self):
                for row in range(self.rows):
                    del self[row][col_index]
                col_index -= 1
            col_index += 1
        try:
            self.__cols = len(self[0])
        except IndexError:
            self.__cols = 0

    def num_of_positive_row(self) -> int:
        """ Get the number of the first row,
        where is a positive item.

        Return -1 if there is no expected row.

        :return: int, number of the row or -1 if there is not.
        """
        for num, row in enumerate(self, 1):
            if any(item > 0 for item in row):
                return num
        return -1

    def __len__(self) -> int:
        """
        :return: int, number of rows.
        """
        return len(self.__matrix)

    def __getitem__(self,
                    index: int) -> List[int]:
        """
        :param index: int, row index.
        :return: list of int, row at the index.
        """
        return self.__matrix[index]

    def __setitem__(self,
                    index: int,
                    new_row: List[int]) -> None:
        """ Set the new row at the index.

        :param index: int, index of the row to change.
        :param new_row: list of int, new row.
        :return: None.
        :exception IndexError: if the index is greater
        or less than matrix length.
        """
        try:
            self.__matrix[index] = new_row
        except IndexError:
            raise IndexError(f"Wrong row index: {index}")

    def __delitem__(self,
                    index: int) -> None:
        """ Delete a row at the index.

        :param index: int, index of the row to delete.
        :return: None.
        """
        try:
            del self.__matrix[index]
        except IndexError:
            raise IndexError(f"Wrong row index: {index}")

    def __str__(self) -> str:
        """ Get str with matrix size, matrix rows and
        num if the first row with a positive item.

        :return: this str.
        """
        positive_row = self.num_of_positive_row()
        if positive_row == -1:
            positive_row = "There is no positive element"
        else:
            positive_row = f"Num of the first row " \
                           f"with a positive item: {positive_row}"
        info = f"Matrix {self.rows} * {self.cols}"
        matrix = '\n'.join(str(row) for row in self)
        return f"{info}\n{matrix}\n{positive_row}"


def main() -> None:
    size = input("Enter the size of the matrix: ").split()
    try:
        size = list(map(int, size))
        assert 0 < len(size) <= 2
        assert all(i > 0 for i in size)
    except ValueError:
        print("Wrong input", file=sys.stderr)
        return
    except AssertionError:
        print("One or two natural values were expected", file=sys.stderr)
        return

    matrix = Matrix(*size)

    # matrix[0] = matrix[2] = matrix[-1] = [0] * matrix.cols

    print(matrix)
    print('_' * 20)
    matrix.remove_zeroes_rows()
    print(matrix)
    print('_' * 20)
    matrix.remove_zeroes_cols()
    print(matrix)
    print('_' * 20)


if __name__ == '__main__':
    main()
