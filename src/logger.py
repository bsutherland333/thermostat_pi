import csv
from datetime import datetime
import os
from typing import List, Tuple, Union


class Logger:
    def __init__(self, filename: str, directory: str, header: list) -> None:
        self._filename = filename
        self._directory = directory
        self._header = header
        self._num_columns = len(header)

    def log(self, data: Union[List, Tuple]) -> None:
        # Check if the data has the correct number of columns
        if len(data) != self._num_columns:
            raise ValueError("Data does not have the correct number of columns")

        # Get the current date and time
        current_date = datetime.now().strftime("%Y_%m_%d")
        current_time = datetime.now().strftime("%H_%M_%S")

        # Get the current time in epoch format
        current_time_epoch = datetime.now().timestamp()

        # Create the full filepath
        appended_filename = f"{self._filename}_{current_date}.csv"
        filepath = os.path.join(self._directory, appended_filename)

        # Create the directory if it does not exist
        os.makedirs(self._directory, exist_ok=True)

        # Open the CSV file in append mode
        with open(filepath, mode="a", newline="") as file:
            writer = csv.writer(file)

            # Write the header if the file is empty
            if file.tell() == 0:
                writer.writerow(["Time", "Epoch Time (s)", *self._header])

            # Write the current time and temperature to the file
            writer.writerow([current_time, current_time_epoch, *data])
