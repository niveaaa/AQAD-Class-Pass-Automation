import serial
from datetime import datetime
from google.oauth2 import service_account
import gspread
import pygame
import os

pygame.mixer.init()

# Define your Google Sheets credentials JSON file path
credentials_file = 'science.json'  # Replace with the path to your service account JSON file

# Define the scope of Google Sheets API you need to access
scope = ['https://www.googleapis.com/auth/spreadsheets']

# Authenticate using service account credentials
credentials = service_account.Credentials.from_service_account_file(
    credentials_file, scopes=scope)

# Open Google Sheets client
gc = gspread.authorize(credentials)

# Open the specific Google Spreadsheet (replace with your spreadsheet ID)
spreadsheet_id = '1aDwjqD7if4tmVn2ZRxjN6BrQ5T8qufQzBBsS2SMD3GU'
sheet = gc.open_by_key(spreadsheet_id).sheet1  # Adjust sheet index if needed

# Define the serial port and baud rate
serial_port = 'COM8'  # Replace with your actual serial port (Windows: 'COMx')
baud_rate = 9600  # Must match the baud rate set in Arduino code

# Open serial port
ser = serial.Serial(serial_port, baud_rate, timeout=1)
print(f"Serial port {serial_port} opened successfully.")

# Initialize the Google Sheet with the headers if needed
sheet.append_row(['Name', 'Time-Out'])
scan_sound = 'scan.mp3'

try:
    while True:
        # Read data from serial port
        line = ser.readline().decode('utf-8').rstrip()
        if line:
            sound = pygame.mixer.Sound(scan_sound)
            sound.play()

            # Debugging output
            print(f"Received: {line}")

            # Process the serial data and match the UID to a name
            name = line

            # Get the current time
            current_time = datetime.now().strftime('%H:%M:%S')  # Get current time only

            # Find if the name already exists in the sheet
            try:
                cell = sheet.find(name)
                # Find the next empty cell in the row
                row_values = sheet.row_values(cell.row)
                next_empty_col = len(row_values) + 1
                sheet.update_cell(cell.row, next_empty_col, current_time)
            except gspread.exceptions.CellNotFound:
                # Name not found, add a new row
                sheet.append_row([name, current_time])

            print(f"Saved to Google Spreadsheet: {name}, {current_time}")

except serial.SerialException as e:
    print(f"Error: {e}")

except KeyboardInterrupt:
    print("Exiting...")

finally:
    ser.close()
    print("Serial port closed.")
