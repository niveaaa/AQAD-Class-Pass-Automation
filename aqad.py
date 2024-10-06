import serial
from datetime import datetime
from google.oauth2 import service_account
import gspread
import pygame

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
spreadsheet_id = '1VDhmvE0dUElPv05FZKqXK43hMF7TkRIaRSLwAIc65aQ'
sheet = gc.open_by_key(spreadsheet_id).sheet1  # Adjust sheet index if needed

# Define the serial port and baud rate
serial_port = 'COM4'  # Replace with your actual serial port (Windows: 'COMx')
baud_rate = 9600  # Must match the baud rate set in Arduino code

# Open serial port
ser = serial.Serial(serial_port, baud_rate, timeout=1)
print(f"Serial port {serial_port} opened successfully.")

# Initialize the Google Sheet with the headers if needed
# sheet.append_row(['Admn No.', 'Answer'])

# Path to sound file
scan_sound = 'scan.mp3'

# Variable to hold the current admission number
current_admission_number = None

try:
    while True:
        # Read data from serial port
        line = ser.readline().decode('utf-8').strip()

        if line:
            # Play sound
            sound = pygame.mixer.Sound(scan_sound)
            sound.play()

            # Debugging output
            print(f"Received: {line}")

            # Process the data
            if line.startswith('Adm'):
                # This is an admission number
                current_admission_number = line
                print(f"Admission Number Received: {current_admission_number}")

                current_admission_number = current_admission_number.replace('Admission Number: ', '')
            
            elif line.startswith('Opt') and current_admission_number:
                # This is an option selected
                option_selected = line.replace('Option Selected: ', '')

                # Write to Google Spreadsheet
                row = [current_admission_number, option_selected]
                sheet.append_row(row, value_input_option='USER_ENTERED')
                print(f"Saved to Google Spreadsheet: {row}")
                # Clear the current admission number
                current_admission_number = None

except serial.SerialException as e:
    print(f"Error: {e}")

except KeyboardInterrupt:
    print("Exiting...")

finally:
    ser.close()
    print("Serial port closed.")
