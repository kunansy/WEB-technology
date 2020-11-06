#!/usr/bin/env python3
import random as rand
import string
from typing import List


COUNTRY_CODES = [1, 7, 9]
DIGITS = list(range(10)) * 7
ALPHABET = string.ascii_lowercase + string.digits


def random_phone() -> str:
    code = rand.choice(COUNTRY_CODES)
    op_code = rand.sample(DIGITS, 3)
    other = rand.sample(DIGITS, 7)

    op_code = ''.join(str(num) for num in op_code)
    other = ''.join(str(num) for num in other)

    return f"{code}{op_code}{other}"


def random_phones(count: int) -> List[int]:
    return [
        random_phone()
        for _ in range(count)
    ]


def random_email() -> str:
    postfixes = [
            '@gmail.com', '@list.ru', '@mail.ru', '@inbox.ru', '@yandex.ru', '@rambler.ru'
    ]
    size = rand.randint(6, 12)

    body = rand.sample(ALPHABET, size)
    body = ''.join(body)

    postfix = rand.choice(postfixes)

    return f"{body}{postfix}"


def random_emails(count: int) -> List[str]:
    return [
        random_email()
        for _ in range(count)
    ]


def main() -> None:
    count = int(input())
    rand_emails = random_emails(count)
    print(*rand_emails, sep='\n')


if __name__ == "__main__":
    main()

