from unittest import TestCase, main
from src.SimpleCSVParser import CSVHandle


class MyTestCase(TestCase):

    def __check_values(self, handle: CSVHandle):
        self.assertEqual(handle[("first", 0)], None)
        self.assertEqual(handle[("second", 0)], "hello;a")
        self.assertEqual(handle[("third", 0)], 3)

        self.assertEqual(handle.get_raw(), [["first", "second", "third"], [None, "hello;a", 3]])

        self.assertEqual(handle.to_string(False), "first;second;third\n;\"hello;a\";3")

    def test_parsing(self):
        handle = CSVHandle("first;second;third\n;\"hello;a\";3", ';')
        self.__check_values(handle)

    def test_init(self):
        handle: CSVHandle = CSVHandle.from_array(
            [["first", "second", "third"], [None, "hello;a", 3]]
        )
        self.__check_values(handle)


if __name__ == '__main__':
    main()
