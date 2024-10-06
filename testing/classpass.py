import serial
import openpyxl
from openpyxl import Workbook
from datetime import datetime
import os

# Configure serial port (adjust these settings as needed)
ser = serial.Serial('COM7', 9600, timeout=1)  # Replace 'COM3' with your serial port

# File name for the Excel file
file_name = 'rfid_log.xlsx'

# Check if the file exists
if not os.path.exists(file_name):
    # Create a new workbook and add a header row if the file doesn't exist
    wb = Workbook()
    ws = wb.active
    ws.title = "RFID Log"
    ws.append(['Name', 'Time'])
    wb.save(file_name)
else:
    # Load the existing workbook
    wb = openpyxl.load_workbook(file_name)
    ws = wb.active

print("Listening for RFID card scans...")

while True:
    if ser.in_waiting > 0:
        name = ser.readline().decode('utf-8').strip()  # Read and decode the serial input
        if name:
            time_str = datetime.now().strftime('%H:%M:%S')  # Get current time only
            ws.append([name, time_str])  # Write to Excel file
            wb.save(file_name)  # Save changes to the file
            print(f"Logged: {time_str} - {name}")
