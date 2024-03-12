from unittest import TestCase, main
from src.SimpleCSVParser import CSVFile


class MyTestCase(TestCase):
    def test_parsing(self):
        file = CSVFile("first;second;third\n;\"hello;a\";3", ';')
        raw = file.get_raw()
        string = file.to_string(False)

        self.assertEqual(file[("first", 0)], None)
        self.assertEqual(file[("second", 0)], "hello;a")
        self.assertEqual(file[("third", 0)], 3)

        self.assertEqual(raw, [["first", "second", "third"], [None, "hello;a", 3]])

        self.assertEqual(string, "first;second;third\n;\"hello;a\";3")


if __name__ == '__main__':
    main()
