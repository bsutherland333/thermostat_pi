import csv
import string
from datetime import datetime


class Logger:
    def __init__(self, filename: string, header: list):
        self.filename = filename
        self.header = header
        self.num_columns = len(header)

        # Create the CSV file if it doesn't exist
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(['Time', 'Epoch Time (s)', *header])

    def log(self, data: list):
        # Check if the data has the correct number of columns
        if len(data) != self.num_columns:
            raise ValueError('Data does not have the correct number of columns')

        # Get the current time
        current_time = datetime.now().strftime('%Y_%m_%d:%H_%M_%S')

        # Get the current time in epoch format
        current_time_epoch = datetime.now().timestamp()

        # Open the CSV file in append mode
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write the current time and temperature to the file
            writer.writerow([current_time, current_time_epoch, *data])
