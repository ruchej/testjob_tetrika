#!/usr/bin/python


def task(arr: str) -> int:
    '''Вернуть индекс первого вхождения искомого символа'''

    return arr.find('0')


def task_2(arr: str) -> int:
    '''
    Вернуть индекс первого вхождения искомого символа
    Второй вариант
    '''
    for i, val in enumerate(arr):
        if val == '0':
            return i

    return -1


print(task('1111111110000000'))
print(task_2('1111111110000000'))

