import xml.etree.ElementTree as ET
import csv
from datetime import datetime

# File paths
input_file = 'input.xml'
output_file = 'processed_readings.csv'

# Parse the XML file
namespace = {'espi': 'http://naesb.org/espi'}
tree = ET.parse(input_file)
root = tree.getroot()

# Open the CSV file for writing
with open(output_file, mode='w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write header
    csv_writer.writerow(['utc_datetime', 'duration', 'cost', 'value'])

    # Extract interval readings
    for interval_reading in root.findall(".//espi:IntervalReading", namespace):
        start_time = interval_reading.find("espi:timePeriod/espi:start", namespace).text
        duration = interval_reading.find("espi:timePeriod/espi:duration", namespace).text
        cost = interval_reading.find("espi:cost", namespace).text
        value = interval_reading.find("espi:value", namespace).text

        # Convert start_time from UNIX timestamp to UTC datetime
        utc_datetime = datetime.utcfromtimestamp(int(start_time)).isoformat()

        # Convert cost and value to correct units
        cost = float(cost) / 100.0
        value = float(value) / 100000.0

        # Write row to CSV
        csv_writer.writerow([utc_datetime, duration, cost, value])

print(f"Processed data has been saved to {output_file}.")
