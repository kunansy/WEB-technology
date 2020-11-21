from random import uniform


def sum_of_positive_nums(arr):
    res = 0
    for i in arr:
        if i > 0:
            res += i
    return res


def max_by_abs(arr):
    mmax = None
    for i in arr:
        if mmax is None or abs(i) > mmax:
            mmax = abs(i)
    return mmax


def min_by_abs(arr):
    mmin = None
    for i in arr:
        if mmin is None or abs(i) < mmin:
            mmin = abs(i)
    return mmin


try:
    n = int(input("Введите n: "))
except ValueError:
    print("Ожидалось число")
    exit(-1)

arr = []
for _ in range(n):
    val = round(uniform(-5, 5), 2)
    arr.append(val)

print(*arr, sep=', ')

print("Сумма положительных элементов =", sum_of_positive_nums(arr))
arr.sort(reverse=True)

mmax = max_by_abs(arr)
mmin = min_by_abs(arr)
mult = 1
print(mmax, mmin)
for i in arr[arr.index(mmax):arr.index(mmin)]:
    mult *= i
print("Произведение:", mult)
print("Отсортированный массив:")
print(*arr, sep=', ')
