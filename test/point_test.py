from functools import cmp_to_key
from unittest import TestCase

import numpy as np
import numpy.ma as ma

from cg.point import Point, turn
from test.utils import is_sorted, get_fall_pos
from cg.utils import PointTestGenerator


class PointTest(TestCase):
    def test_add_eq(self):
        print('\n...addition random tests...')
        for i, (p1, p2) in enumerate(zip(PointTestGenerator.generateInteger(),
                                         PointTestGenerator.generateInteger())):
            self.assertTrue(Point(p1) + Point(p2) == Point(p1 + p2), 'invalid __add__ and __eq__ methods.')
        PointTestGenerator.cumulativeTestCount += i + 1

    def test_sub_eq(self):
        print('\n...subtraction random tests...')
        for i, (p1, p2) in enumerate(zip(PointTestGenerator.generateInteger(),
                                         PointTestGenerator.generateInteger())):
            self.assertTrue(Point(p1) - Point(p2) == Point(p1 - p2), 'invalid __sub__ and __eq__ methods.')
        PointTestGenerator.cumulativeTestCount += i + 1

    def test_neg_eq(self):
        print('\n...negation random tests...')
        for i, p in enumerate(PointTestGenerator.generateInteger()):
            self.assertTrue(-Point(p) == Point(-p), 'invalid __neg__ and __eq__ methods.')
        PointTestGenerator.cumulativeTestCount += i + 1

    def test_mul_eq(self):
        print('\n...multiplication random tests...')
        for i, p in enumerate(PointTestGenerator.generateInteger()):
            value = np.random.randint(0, 100, 1)
            self.assertTrue(Point(p) * value == Point(p * value), 'invalid __mul__ and __eq__ methods.')
        PointTestGenerator.cumulativeTestCount += i + 1

    def test_le(self):
        print('\n...less random tests...')
        for i, (p1, p2) in enumerate(zip(PointTestGenerator.generateInteger(),
                                         PointTestGenerator.generateInteger())):
            p2 = ma.array(np.abs(p2), dtype=np.int64)
            p = Point(p1)
            for dim in range(len(p1)):
                p2.mask = np.logical_or(np.arange(len(p1)) < dim,
                                        np.random.randint(2, size=len(p1)).astype(np.bool))
                p3 = Point(p2.filled(0) + p1)
                self.assertTrue(p <= p3, 'invalid __lt__ method')
        PointTestGenerator.cumulativeTestCount += i + 1

    def test_turn(self):
        print('\n...turn tests with unit circle...')
        # Now we have only 2-dimensional turn tests
        # TODO: n-dimensional turn test
        # main idea: get n points from unit circle and sort it by turn predicate
        return
        # todo: ТЕСТЫ
        for n in range(6, 50):
            points = np.roots([1] + [0] * (n - 1) + [1])
            points = np.arange()
            points = np.random.permutation(np.array([np.real(points), np.imag(points)]).T)
            points = list(map(Point, points))
            points = [points[0]] + sorted(points[1:], key=cmp_to_key(lambda x, y: turn(points[0], x, y)))
            points = np.array([pt.coord for pt in points])
            points = points.T[0] + 1j * points.T[1]
            points = np.real(np.log(points) / (np.pi * 1j) * n)
            self.assertTrue(is_sorted(np.roll(points, n - 1 - get_fall_pos(points))), 'invalid turn predicate')
        PointTestGenerator.cumulativeTestCount += 1

    def tearDown(self):
        print('...passed %d tests...' % PointTestGenerator.cumulativeTestCount)
