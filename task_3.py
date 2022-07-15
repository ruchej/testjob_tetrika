from typing import Optional

from requests.api import patch


def crossing(t1: list[int], t2: list[int]) -> Optional[tuple]:
    '''Вернуть пересечение двух интервалов'''
    s1, e1 = t1
    s2, e2 = t2
    if s1 <= e2 and e1 >= s2:
        start = max(s1, s2)
        end = min(e1, e2)
        return start, end
    return None


def chain_intersections(t1: list[int], t2: list[int]) -> list:
    '''Вернуть список пересечений интервалов'''
    cross_time = []
    for s1, e1 in zip(*[iter(t1)] * 2):
        for s2, e2 in zip(*[iter(t2)] * 2):
            cross = crossing([s1, e1], [s2, e2])
            if cross:
                cross_time.extend(cross)
    return cross_time


def sum_intervals(intervals: list) -> int:
    '''Вернуть сумму интервалов'''
    times = []
    for s, e in zip(*[iter(intervals)] * 2):
        times.append(e-s)
    return sum(times)


def gluin_intervals(t: list[int]) -> list[int]:
    '''Склеить интервалы, которые имеют пересечение'''
    pairs = list(zip(*[iter(t)] * 2))
    pairs.sort(key=lambda x: x[0])
    gluing = []
    i = 0
    while i < len(pairs):
        if i+1 < len(pairs):
            s1, e1 = pairs[i]
            s2, e2 = pairs[i+1]
            if s2 < e1:
                s, e = s1, max(e1, e2)
                pairs[i] = (s, e)
                pairs.pop(i+1)
                t = gluin_intervals([x for y in pairs for x in y])
                pairs = list(zip(*[iter(t)] * 2))
        gluing.extend(pairs[i])
        i += 1
    return gluing


def appearance(intervals):
    '''Найти пересечения интервалов и вернуть общее время'''
    lesson = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']
    cross_pupil_tutor = chain_intersections(gluin_intervals(pupil), gluin_intervals(tutor))
    cross_lesson = chain_intersections(lesson, cross_pupil_tutor)
    return sum_intervals(cross_lesson)


tests = [
    {
        'data': {
            'lesson': [1594663200, 1594666800],
            'pupil': [
                1594663340,
                1594663389,
                1594663390,
                1594663395,
                1594663396,
                1594666472,
            ],
            'tutor': [1594663290, 1594663430, 1594663443, 1594666473],
        },
        'answer': 3117,
    },
    {
        'data': {
            'lesson': [1594702800, 1594706400],
            'pupil': [
                1594702789,
                1594704500,
                1594702807,
                1594704542,
                1594704512,
                1594704513,
                1594704564,
                1594705150,
                1594704581,
                1594704582,
                1594704734,
                1594705009,
                1594705095,
                1594705096,
                1594705106,
                1594706480,
                1594705158,
                1594705773,
                1594705849,
                1594706480,
                1594706500,
                1594706875,
                1594706502,
                1594706503,
                1594706524,
                1594706524,
                1594706579,
                1594706641,
            ],
            'tutor': [
                1594700035,
                1594700364,
                1594702749,
                1594705148,
                1594705149,
                1594706463,
            ],
        },
        'answer': 3577,
    },
    {
        'data': {
            'lesson': [1594692000, 1594695600],
            'pupil': [1594692033, 1594696347],
            'tutor': [1594692017, 1594692066, 1594692068, 1594696341],
        },
        'answer': 3565,
    },
]


if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['data'])
       print(f'Рассчёт: {test_answer} Ответ: {test["answer"]}')
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

