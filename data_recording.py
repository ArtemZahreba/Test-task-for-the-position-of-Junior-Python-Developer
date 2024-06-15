"""
This code implements data recording into a database and Excel format.
Everything is implemented within a class.
"""

# Import necessary libraries for calculations, working with databases, Excel, and time
import pandas as pd
import xlsxwriter
import sqlite3
from datetime import datetime

class DataRecording():
    """
    This class is implemented for data recording.

    It works with the 'data' directory.

    It has three functions:
    - To create an Excel file with a header.
    - To append data to the Excel file.
    - To add data to the database.
    """

    def __init__(self):
        self._curr_data = datetime.now().strftime('%Y-%m-%d')
        self._file_name = f'data/vacancies_{self._curr_data}.xlsx'
        self._bd = 'count_data.db'

    def get_curr_data(self) -> str:
        """
        This is a getter function that updates and returns the value of _curr_data.

        :return: Current date as a string.
        """
        return self._curr_data

    def set_curr_data(self) -> None:
        """
        Function to update the value of _curr_data.

        :return: None
        """
        self._curr_data = datetime.now().strftime('%Y-%m-%d')

    def get_file_name(self) -> str:
        """
        Function to return the value of _file_name, which is the directory and file name.

        :return: File name as a string.
        """
        return self._file_name

    def set_file_name(self) -> None:
        """
        Function to set the value of _file_name.

        :return: None
        """
        self._file_name = f'data/vacancies_{self._curr_data}.xlsx'

    def create_excel_with_header(self) -> None:
        """
        Function to create an Excel file and add a header to the table.

        :return: None
        """
        # Create a new Excel file and add a worksheet
        workbook = xlsxwriter.Workbook(self._file_name)
        worksheet = workbook.add_worksheet()

        # Create the table header
        header = ['datetime', 'vacancy_count', 'change']

        # Write the table header to the first row
        for col_num, header_title in enumerate(header):
            worksheet.write(0, col_num, header_title)

        # Set the column width for columns A, B, and C to 20
        worksheet.set_column('A:C', 20)

        # Close the file to save changes
        workbook.close()

    def append_data_to_excel(self, datetime_value, vacancy_count) -> None:
        """
        Function to add data to the file and calculate the difference between vacancy counts.

        :param datetime_value: The current date and time.
        :param vacancy_count: The number of vacancies.
        :return: None
        """
        # Load the existing file
        try:
            df = pd.read_excel(self._file_name)
        except FileNotFoundError:
            # If the file is not found, create it with a header
            self.create_excel_with_header()
            df = pd.read_excel(self._file_name)

        # Calculate the change (difference)
        if len(df) == 0:
            change = 0
        else:
            change = vacancy_count - df['vacancy_count'].iloc[-1]

        # Add a new row
        new_row = pd.DataFrame({'datetime': [datetime_value], 'vacancy_count': [vacancy_count], 'change': [change]})
        df = pd.concat([df, new_row], ignore_index=True)

        # Write the updated data back to the file
        df.to_excel(self._file_name, index=False)

    def insert_data_into_vacancies_table(self, timestamp, vacancies_count) -> None:
        """
        Function to add data to the database.

        :param timestamp: The current timestamp.
        :param vacancies_count: The number of vacancies.
        :return: None
        """
        # Connect to the database
        conn = sqlite3.connect(self._bd)
        cursor = conn.cursor()

        # Create the table if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS vacancies (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          timestamp TEXT NOT NULL,
                          vacancies_count INTEGER
                          );
                       ''')

        # Execute the query to insert data
        cursor.execute(
            "INSERT INTO vacancies (timestamp, vacancies_count) VALUES (?, ?)",
            (timestamp, vacancies_count))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
