import csv

import mysql.connector

# Database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ray_930715",
    database="traffic_enforcements"
)

cursor = db_connection.cursor()

# SQL query to select specific columns
query = """
SELECT id, location, speed_limit, current_speed, cam_id, date_time, longitude, latitude, recognition, error_code, ticket
FROM violation_records
"""

cursor.execute(query)
rows = cursor.fetchall()

# CSV file path
csv_file_path = r'C:\Users\USER\Desktop\traffic_enforcement\violation_records.csv'

# Writing to CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Writing the header
    writer.writerow(['id', 'location', 'speed_limit', 'current_speed', 'cam_id', 'date_time', 'longitude', 'latitude', 'recognition', 'error_code', 'ticket'])
    # Writing the data
    writer.writerows(rows)
ImportWarning
# Function to extract district from location
def extract_district(location):
    if "大同區" in location:
        return "大同區"
    elif "南港區" in location:
        return "南港區"
    elif "松山區" in location:
        return "松山區"
    elif "萬華區" in location:
        return "萬華區"
    elif "信義區" in location:
        return "信義區"
    elif "大安區" in location:
        return "大安區"
    elif "中山區" in location:
        return "中山區"
    elif "士林區" in location:
        return "士林區"
    elif "中正區" in location:
        return "中正區"
    else:
        return "未知區"

# Adding district to each row
rows_with_district = []
for row in rows:
    location = row[1]
    district = extract_district(location)
    rows_with_district.append(row + (district,))

# Writing to CSV file with district column
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Writing the header
    writer.writerow(['id', 'location', 'speed_limit', 'current_speed', 'cam_id', 'date_time', 'longitude', 'latitude', 'recognition', 'error_code', 'ticket', 'district'])
    # Writing the data
    writer.writerows(rows_with_district)
# Closing the cursor and connection
cursor.close()
db_connection.close()