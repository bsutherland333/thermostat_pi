import csv
import string
from datetime import datetime


def log_data(data: float, filename: string):
    # Get the current time
    current_time = datetime.now().strftime('%_%_%:%_%_%')

    # Open the CSV file in append mode
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)

        # If the file is empty, write the header
        if file.tell() == 0:
            writer.writerow(['Time', 'Temperature'])

        # Write the current time and temperature to the file
        writer.writerow([current_time, data])
