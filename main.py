"""
This code implements a program for asynchronous data parsing and recording.
"""

# Imports for data collection, processing, recording, asynchronicity, working with directories, and dates
from parse_data import ParseData
from data_recording import DataRecording
from datetime import datetime
import asyncio
import os

class MainProgram():
    """
    This class implements the main program. The primary function of the class is the `run` method,
    which collects data every hour and records it in the appropriate formats.
    """

    def __init__(self):
        self._parse_robota = ParseData()
        self._data_rec = DataRecording()
        self.curr_date = datetime.now().strftime('%Y-%m-%d')

    def get_curr_date(self):
        """
        Function to return the current year, month, and date.

        :return: Current date as a string.
        """
        return self.curr_date

    def set_curr_date(self):
        """
        Function to set the current year, month, and date.

        :return: None
        """
        self.curr_date = datetime.now().strftime('%Y-%m-%d')

    def get_file(self):
        """
        Function to return the shortened path to the Excel file.

        :return: Path to the Excel file as a string.
        """
        return self._data_rec.get_file_name()

    def check_file_exists(self, file_path):
        """
        Function to check if a file exists in the directory.

        :param file_path: Path to the file.
        :return: True if file exists, False otherwise.
        """
        return os.path.exists(file_path)

    def set_config(self):
        """
        Function to set the values for the current date and file name in the DataRecording class.

        :return: None
        """
        self._data_rec.set_curr_data()
        self._data_rec.set_file_name()

    async def run(self):
        """
        Main function of the program, which runs asynchronously, allowing it to execute every hour.

        :return: None
        """
        while True:
            # Create variables needed for further work
            # Current date and time rounded to the nearest hour for recording
            current_time = datetime.now().strftime("%Y-%m-%d %H:00")
            # Current date for further verification
            current_date = self.get_curr_date()

            # Date in the DataRecording instance for further verification
            date_in_records = self._data_rec.get_curr_data()
            # Path to the folder with the file
            folder = self._data_rec.get_file_name()

            # Number of vacancies
            vacancies_count = self._parse_robota.get_count()

            # Check if the file exists in the folder or if the date matches; if not, create a new Excel file
            if not self.check_file_exists(folder) or current_date != date_in_records:
                # Update date and file path in the DataRecording class
                self.set_config()
                # Call function to create a table with a header
                self._data_rec.create_excel_with_header()
                # Add data to the table
                self._data_rec.append_data_to_excel(
                    datetime_value=current_time,
                    vacancy_count=vacancies_count
                )
            else:
                # If the file exists and the current date matches the date in the records, just append the data
                self._data_rec.append_data_to_excel(
                    datetime_value=current_time,
                    vacancy_count=vacancies_count
                )
            # Insert data into the database
            self._data_rec.insert_data_into_vacancies_table(
                timestamp=current_time,
                vacancies_count=vacancies_count
            )

            # Repeat the procedure in an hour
            await asyncio.sleep(60 * 60)  # 60 minutes * 60 seconds = 1 hour

    def start(self):
        """
        Function to start the program.

        :return: None
        """
        asyncio.run(self.run())
