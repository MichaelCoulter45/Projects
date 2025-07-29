import xml.etree.ElementTree as ET
from datetime import datetime
import csv
import math

file_path = r"C:\Users\power\git\Projects\Running Dashboard\parse_me.tcx"

tree = ET.parse(file_path)
root = tree.getroot()
ns = {'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
trackpoints = root.findall('.//tcx:Trackpoint', ns)

data = []
start_time = None
prev_time = None
prev_distance_km = 0
prev_distance_mi = 0
mph = None
kpm = None
avg_pace = None
avg_hr = 0
max_hr = None
hr_cumulative = 0
count = 0
fastest_1_mile = None
split_200m = None
split_400m = None
split_800m = None
split_1000m = None
split_1_mile = None
split_2_miles = None
split_5k = None
split_10k = None
split_10_miles = None
split_half_marathon = None
split_15_miles = None
split_20_miles = None
split_marathon = None
split_30_miles = None

def is_not_None(is_this_None):
    if is_this_None != None:
        return False
    return True

def format_pace(pace_float):
    if pace_float is None or pace_float == 0:
        return None
    minutes = int(pace_float)
    seconds = int(round((pace_float - minutes) * 60))
    if seconds == 60:
        minutes += 1
        seconds = 0
    return f"{minutes}:{seconds:02d}"

def elapsed_time(curr_time, start_time):
    if curr_time is not None and start_time is not None:
        return curr_time - start_time
    return -1

def format_time(date_time):
    if is_not_None(date_time):
        return date_time.strftime('%H:%M:%S')

def convert_meters_to_miles(meters):
    if meters is not None:
        return round(meters / 1.60934, 4)
    return -1
    
def convert_miles_to_meters(miles):
    if miles is not None:
        return round((miles / 0.62137273) * 1000, 4) #Convers miles to kilometers then ( *1000) to meters
    return -1

###########################################
#START OF MAIN TRACKPOINT FOR-LOOP
for tp in trackpoints:
    time_elem = tp.find('tcx:Time', ns)
    hr_elem = tp.find('.//tcx:HeartRateBpm/tcx:Value', ns)
    distance_elem = tp.find('tcx:DistanceMeters', ns)
    elevation_elem= tp.find('tcx:AltitudeMeters', ns)
    cadence_elem = tp.find('tcx:Cadence', ns)
    
    curr_time = None
    heart_rate = None
    distance_km = None
    distance_mi = None
    pace_km = None
    pace_mi = None
    elevation_m = None
    cadence = None
    split_distance = None
    
    if time_elem is not None:
        time_str = time_elem.text
        curr_time = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        
        if start_time is None:
            start_time = curr_time
            
        elapsed = curr_time - start_time
        elapsed_str = str(elapsed).split('.')[0] #Returns hh:mm:ss and trims the microseconds
        time_format = curr_time.strftime('%H:%M:%S')
        
    if hr_elem is not None:
        heart_rate = int(hr_elem.text)
        hr_cumulative += heart_rate
        if max_hr == None or heart_rate > max_hr:
            max_hr = heart_rate
        
    if distance_elem is not None:
        distance_km = float(distance_elem.text) / 1000
        distance_mi = distance_km / 1.60934
        
    if elevation_elem is not None:
        elevation_m = float(elevation_elem.text)
        
    if cadence_elem is not None:
        cadence = int(cadence_elem.text) * 2 #TCX measures 1 leg, so * 2 counts for both legs.
        
    #Calculating paces:
    if (
        curr_time is not None and
        distance_km is not None and
        distance_mi is not None and
        prev_time is not None and
        prev_distance_km is not None and
        prev_distance_mi is not None
    ):
        time_diff_min = (curr_time - prev_time).total_seconds() / 60 # --> Minutes
        time_diff_hr = (curr_time - prev_time).total_seconds() / 3600 # --> Hours
        dist_diff_km = distance_km - prev_distance_km
        dist_diff_mi = distance_mi - prev_distance_mi
        if dist_diff_km > 0.0015: #finding pace km (min/km)
            pace_km = time_diff_min / dist_diff_km
        if dist_diff_mi > 0.0015: #finding pace mi (min/mile)
            pace_mi = time_diff_min / dist_diff_mi
        if time_diff_hr > 0 and dist_diff_mi > 0: #finding mph
            mph = dist_diff_mi / time_diff_hr
        if time_diff_hr > 0 and dist_diff_km > 0: #finding kpm
            kpm = dist_diff_km / time_diff_hr

    # calculate prev_distance_mi
    if distance_mi is not None:
        prev_distance_mi = distance_mi
    # calculate prev_distance_km
    if distance_km is not None:
        prev_distance_km = distance_km
        
    # Gathering split datas:
    if distance_elem is not None:
        split_distance = int(distance_elem.text)
    if split_distance is not None:
        if split_200m == None and split_distance >= 200:
            split_200m = elapsed_time(curr_time, start_time)
            
        if split_400m == None and split_distance >= 400:
            split_400m = curr_time
            
        if split_800m == None and split_distance >= 800:
            split_800m = curr_time
            
        if split_1_mile == None and split_distance >= 1609:
            split_1_mile = curr_time
            
        if split_2_miles == None and split_distance >= 3218:
            split_200m = curr_time
            
        if split_5k == None and split_distance >= 5000:
            split_5k = curr_time
            
        if split_10k == None and split_distance >= 10000:
            split_10k = curr_time
            
        if split_10_miles == None and split_distance >= 16093:
            split_10_miles = curr_time
            
        if split_half_marathon == None and split_distance >= 21100:
            split_half_marathon = curr_time
            
        if split_15_miles == None and split_distance >= 24140:
            split_15_miles = curr_time
            
        if split_20_miles == None and split_distance >= 32186:
            split_20_miles = curr_time
            
        if split_marathon == None and split_distance >= 42197:
            split_marathon = curr_time
            
        if split_30_miles == None and split_distance >= 48280:
            split_30_miles = curr_time
    
# if split_200m:
#     print(f"Fastest 200m: {split_200m}")
# if split_400m:
#     print(f"Fastest 400m: {split_400m}")
# if split_800m:
#     print(f"Fastest 800m: {split_800m}")
# if split_1000m:
#     print(f"Fastest 1000m: {split_1000m}")
# if split_1_mile:
#     print(f"Fastest Mile: {split_1_mile}")
# if split_2_miles:
#     print(f"Split 2 Miles: {split_2_miles}")
# if split_5k:
#     print(f"Split 5k: {split_5k}")
# if split_10k:
#     print(f"Split 10k: {split_10k}")
# if split_10_miles:
#     print(f"Split 10 Miles: {split_10_miles}")
# if split_half_marathon:
#     print(f"Split 13.1 Miles: {split_half_marathon}")
# if split_15_miles:
#     print(f"Split 15 Miles: {split_15_miles}")
# if split_20_miles:
#     print(f"Split 20 Miles: {split_20_miles}")
# if split_marathon:
#     print(f"Split 26.2 Miles: {split_marathon}")
# if split_30_miles:
#     print(f"Split 26.2 Miles: {split_30_miles}")
    
    entry = {
        "Time": elapsed_str,
        "Heart Rate": heart_rate,
        "Distance (mi)": round(distance_mi, 2) if distance_mi is not None else None,
        "Pace (min/mi)": format_pace(pace_mi),
        "Miles per Hour": round(mph, 2) if mph is not None else None,
        "Distance (km)": distance_km,
        "Pace (min/km)": format_pace(pace_km),
        "Kilometers per Hour": round(kpm, 2) if kpm is not None else None,
        "Elevation (m)": round(elevation_m, 1) if elevation_m is not None else None,
        "Cadence": cadence
    }
    
    data.append(entry)
    
    prev_time = curr_time
    prev_distance_km = distance_km
    count += 1
#END OF MAIN TRACKPOINT FOR-LOOP
##########################################

#Finding total distances:
if data: #checks if data exists in the case the file is empty. Prevents a crash.
    total_distance_km = data[-1]["Distance (km)"]
    total_distance_mi = round(total_distance_km / 1.60934, 2)

#Finding average pace:

#Finding total time after the loop completes:
end_time = curr_time

if start_time is not None and end_time is not None:
    total_duration = end_time - start_time
    total_seconds = total_duration.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    total_duration_str = str(total_duration).split('.')[0]
else:
    total_duration_str = "N/A"
    minutes = seconds = 0

#Display average heart rate:
if hr_cumulative > 0:
    avg_hr = int(hr_cumulative / sum(1 for d in data if d["Heart Rate"] is not None))

#Preview the first [:X] entries
for entry in data[:0]:
    print(entry)

output_file = "parsed_run_data.csv"

with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Time",
        "Heart Rate", 
        "Distance (mi)",
        "Pace (min/mi)",
        "Miles per Hour",
        "Distance (km)", 
        "Pace (min/km)",
        "Kilometers per Hour",
        "Elevation (m)",
        "Cadence"
        ])
    writer.writeheader()

    for row in data:
        writer.writerow(row)



print(f"Saved {len(data)} rows to {output_file}")


print(f"\n=== Run Summary ===")
print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S') if start_time else 'N/A'}")
print(f"Total Distance: {total_distance_km:.2f} km / {total_distance_mi:.2f} mi")
print(f"Total Time: {total_duration_str}")
#print(f"Acitivty Time: {activity_duration_str}")
print(f"Total Minutes: {minutes}:{seconds:02d}")
#print(f"Average Pace: ")
print(f"Average Heart Rate: {avg_hr}")
print(f"Max Heart Rate: {max_hr}")


if fastest_1_mile:
    print(f"Fastest Mile: {fastest_1_mile}")
if split_200m:
    print(f"Split 200m: {format_time(split_200m)}")
if split_400m:
    print(f"Split 400m: {split_400m}")
if split_800m:
    print(f"Split 800m: {split_800m}")
if split_1000m:
    print(f"Split 1000m: {split_1000m}")
if split_2_miles:
    print(f"Split 2 Miles: {split_2_miles}")
if split_5k:
    print(f"Split 5k: {split_5k}")
if split_10k:
    print(f"Split 10k: {split_10k}")
if split_10_miles:
    print(f"Split 10 Miles: {split_10_miles}")
if split_half_marathon:
    print(f"Split 13.1 Miles: {split_half_marathon}")
if split_15_miles:
    print(f"Split 15 Miles: {split_15_miles}")
if split_20_miles:
    print(f"Split 20 Miles: {split_20_miles}")
if split_marathon:
    print(f"Split 26.2 Miles: {split_marathon}")
if split_30_miles:
    print(f"Split 26.2 Miles: {split_30_miles}")