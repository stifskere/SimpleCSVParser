from re import match, sub, IGNORECASE
from locale import localeconv, setlocale, LC_ALL


class CSVInitError(Exception):
    def __init__(self, what: str):
        super().__init__(what)


class CSVHandle:
    """Represents a CSV handle."""

    __parsed: list[list[str | int | type(None)]]
    __separator: str

    @staticmethod
    def __get_list_separator() -> str:
        setlocale(LC_ALL, "")
        return ';' if localeconv()["decimal_point"] == ',' else ','

    @staticmethod
    def __split_at_level(to_split: str, separator: str) -> list[str]:
        result: list[str] = []

        is_in_string: bool = False
        current: str = ""
        for char in to_split:
            if char == '"':
                is_in_string = not is_in_string
            elif char == separator and not is_in_string:
                result.append(current)
                current = ""
            else:
                current += char

        result.append(current)

        if to_split[len(to_split) - 1] == separator:
            result.append("")

        return result

    @staticmethod
    def __cast_results(set_of_results: list[list[str | int | type(None)]]) \
            -> list[list[str | int | type(None)]]:
        result: list[list[str | int | type(None)]] = []

        for row in set_of_results:
            sub_result: list[str | int | type(None)] = []
            for value in row:
                if value.isnumeric():
                    sub_result.append(int(value))
                elif sub("[.,]", "", value).isnumeric():
                    sub_result.append(float(value))
                elif len(value) == 0:
                    sub_result.append(None)
                else:
                    sub_result.append(value)
            result.append(sub_result)

        return result

    def __init__(self, to_parse: str, separator: str = None):
        """Create a new instance from a string and specify a separator."""
        separated_result: list[list[str]] = []
        lines: list[str] = to_parse.splitlines()

        had_separator: bool = False
        if len(to_parse) > 0:
            if match_separator := match("^[^=]+=(?P<separator>[^\n\r ])$", lines[0], IGNORECASE):
                if separator is None:
                    separator = match_separator.group("separator")
                had_separator = True
        elif separator is None or len(to_parse) <= 0:
            separator = self.__get_list_separator()

        length: int | type(None) = None
        for row in lines[1 if had_separator else 0:]:
            split: list[str] = self.__split_at_level(row, separator)
            if length is None:
                length = len(split)
            elif len(split) != length:
                raise CSVInitError("Cannot initialize an instance of CSVParser with an invalid CSV string.")
            separated_result.append(split)

        self.__separator = separator
        self.__parsed = self.__cast_results(separated_result)

    @staticmethod
    def from_file(path: str, separator: str = None):
        """Create a new instance of CSVFile from a file."""
        with open(path, "r") as file:
            return CSVHandle(file.read(), separator)

    @staticmethod
    def from_array(arr: list[list[int | str | type(None)]]):
        """Initialize a new instance of CSVHandle from a list."""
        for row in arr:
            if not isinstance(row, list):
                raise CSVInitError("A list was found containing something else than list[int|str|NoneType]")

            # this is done for line length sake :)
            for element in row:
                if not isinstance(element, str):
                    if not isinstance(element, int):
                        if not isinstance(element, float):
                            if not isinstance(element, type(None)):
                                raise CSVInitError("element")

            instance: CSVHandle = CSVHandle("")
            instance.__parsed = arr
            return instance

    def __get_index(self, column_name: str) -> int:
        for index, name in enumerate(self.__parsed[0]):
            if name == column_name:
                return index

        return -1

    def __getitem__(self, position: tuple[str, int]) -> int | str | type(None):
        """Obtain an item from the parsed CSV object."""
        column, index = position

        column_index: int = self.__get_index(column)

        if column_index == -1:
            raise IndexError("Column was not found.")

        return self.__parsed[index + 1][column_index]

    def get_raw(self) -> list[list[int | str | type(None)]]:
        """Obtain the parsed CSV list generated from the parsed CSV."""
        return self.__parsed

    def to_string(self, specify_separator: bool = True) -> str:
        """Convert this instance of CSV to a string."""
        result: str = f"sep={self.__separator}\n" if specify_separator else ""

        for line in self.__parsed:
            for value in line:
                if self.__separator in str(value):
                    value = f"\"{value}\""

                if value is None:
                    value = ""

                result += f"{value}{self.__separator}"

            result = f"{result[:-1]}\n"

        return result[:-1]

    def write_to_file(self, path: str, specify_separator: bool = True) -> None:
        """Write a string representation of this CSV to a file."""
        with open(path, "w") as file:
            file.write(self.to_string(specify_separator))
