# Simple CSV parser

> [!warning]
> **This library is now unmaintained** and it's use is not recommended, I don't update this anymore, the use of the
> [**python's CSV api**](https://docs.python.org/3/library/csv.html) is advised.

This is a simple package designed to serialize and deserialize CSV.

### Installing

Use Python PIP

```bash
pip install SimpleCSVParser
```

### Usage

The package contains a single class which is `CSVFile` that represents a CSV file.

```py
# you can use CSVInitError for catching exceptions, 
# it's the only exception thrown by the library.
from SimpleCSVParser import CSVHandle, CSVInitError


# create a new instance from a file.
parsed_csv: CSVHandle = CSVHandle.from_file("my_csv_file.csv")
# you can also create a new instance from a raw string.
parsed_csv = CSVHandle("your;csv;here\n1;2;3")

# You can also specify the separator in a second arugment.
parsed_csv: CSVHandle = CSVHandle.from_file("my_csv_file.csv", ';')
parsed_csv = CSVHandle("your;csv;here\n1;2;3", ';')

# or initializing from an array
parsed_csv: CSVHandle = CSVHandle.from_array(["first", "second"], [1, 2])

# Obtain a specific element, the second argument being 
# the row number not taking the column name into account.
parsed_csv[("Column Name", 0)]

# Obtain a list[list[any]] of the serialized CSV, the first
# column being the column names so, row[column[any]].
parsed_csv.get_raw()

# Obtain a string from the CSV instance.
parsed_csv.to_string()

# You can optionally specify if it's going to add the 
# separator specifier if so, it's going to append 
# "sep={separator}" to the start.
parsed_csv.to_string(True) # default being true.

# There is also a shortcut for writing the CSV to a file.
parsed_csv.write_to_file("./path_to_file.csv")

# And of course define if it's going to specify the separator.
parsed_csv.write_to_file("./path_to_file.csv", True) # default being true.
```

### Contributing

You can make a pull request, and it will be checked as soon as possible.

