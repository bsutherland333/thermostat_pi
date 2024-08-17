import csv
import os
import string
from datetime import datetime


class Logger:
    def __init__(self, filename: string, filepath: string, header: list):
        self.filename = filename
        self.filepath = filepath
        self.header = header
        self.num_columns = len(header)

    def log(self, data: list):
        # Check if the data has the correct number of columns
        if len(data) != self.num_columns:
            raise ValueError("Data does not have the correct number of columns")

        # Get the current date and time
        current_date = datetime.now().strftime("%Y_%m_%d")
        current_time = datetime.now().strftime("%H_%M_%S")

        # Get the current time in epoch format
        current_time_epoch = datetime.now().timestamp()

        # Create the full filepath
        appended_filename = f"{self.filename}_{current_date}.csv"
        full_filepath = os.path.join(self.filepath, appended_filename)

        # Open the CSV file in append mode
        with open(full_filepath, mode="a", newline="") as file:
            writer = csv.writer(file)

            # Write the header if the file is empty
            if file.tell() == 0:
                writer.writerow(["Time", "Epoch Time (s)", *header])

            # Write the current time and temperature to the file
            writer.writerow([current_time, current_time_epoch, *data])
