import serial
import csv
from datetime import datetime
from time import sleep
from CountdownTester import loading_bar

# Serial port configuration
SERIAL_PORT = '/dev/cu.usbmodem11301'  # Change this to match your Arduino's port
BAUD_RATE = 115200  # Make sure this matches your Arduino's baud rate

# CSV file configuration
CSV_FILENAME = f"load_cell_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"


def countdown_func():
    seconds = 5
    while (seconds < 6) and (seconds > 0):
        sleep(1)
        print(f"Starting data recording in {seconds} seconds")
        seconds -= 1
    print("Data recording has started: ")


def main():
    try:
        # Open serial port
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Connected to {SERIAL_PORT}")

            # Open CSV file
            with open(CSV_FILENAME, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Timestamp', 'Weight'])  # Write header

                print(f"Saving data to {CSV_FILENAME}")
                print("Press Ctrl+C to stop...")

                loading_bar()
                

                while True:
                    # Read a line from the serial port
                    line = ser.readline().decode('utf-8').strip()

                    if line:
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                        weight = float(line)

                        # Write to CSV
                        csv_writer.writerow([timestamp, weight]) ##weight should be printer in terms of newtons.

                        # Print to console
                        print(f"{timestamp}: {weight}")

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    except KeyboardInterrupt:
        print("\nData collection stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    countdown_func()
    main()
    print(CSV_FILENAME)
    print("done")

