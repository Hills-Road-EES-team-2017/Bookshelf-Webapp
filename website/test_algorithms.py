import unittest
import algorithms

class Fake_book:
    def __init__(self, width):
        self.width = width

class Fake_partition:
    def __init__(self, space=0, distance=0):
        self.space = space
        self.distance = distance


class TestFind_partition_for_returning_book(unittest.TestCase):
    def test_trivial(self):
        books = [Fake_book(width=10)]
        partitions = [Fake_partition(space=15)]
        results = algorithms.find_partitions_for_returning_books(books, partitions)
        self.assertEqual(results, partitions)

    def test_partition_per_book(self):
        books = [Fake_book(width=10), Fake_book(width=12)]
        partitions = [Fake_partition(space=150)]
        results = algorithms.find_partitions_for_returning_books(books, partitions)
        self.assertEqual(results, [partitions[0],partitions[0]])

    def test_closest_partition(self):
        books = [Fake_book(width=10), Fake_book(width=12)]
        partitions = [Fake_partition(space=150, distance=15), Fake_partition(space=150, distance=10)]
        results = algorithms.find_partitions_for_returning_books(books, partitions)
        self.assertEqual(results, [partitions[1], partitions[1]])

    def test_partition_with_space(self):
        books = [Fake_book(width=10)]
        partitions = [Fake_partition(space=9, distance=10), Fake_partition(space=11, distance=15)]
        results = algorithms.find_partitions_for_returning_books(books, partitions)
        self.assertEqual(results, [partitions[1]])

    def test_partition_with_space_decreasing(self):
        books = [Fake_book(width=10), Fake_book(width=10)]
        partitions = [Fake_partition(space=15, distance=15), Fake_partition(space=15, distance=10)]
        results = algorithms.find_partitions_for_returning_books(books, partitions)
        self.assertEqual(results, [partitions[1], partitions[0]])


if __name__ == '__main__':
    unittest.main()
