import requests
import csv
import os
import time
from datetime import datetime

API_KEY = "81f010e7-3a8f-449c-8874-0d777a6f00da"  

url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json"
params = {
    "key": API_KEY,
    "LineRef": "Q18",
    "VehicleMonitoringDetailLevel": "calls"
}

FILE = "q18_data_v2.csv"
HEADER = ["polled_at", "recorded_at", "bus_id", "direction", "lat", "lon",
          "stop_id", "stop_name", "distance_m", "stops_away",
          "expected_arrival", "presentable_distance"]

# Write the header row only if the file is new
if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        csv.writer(f).writerow(HEADER)

while True:
    response = requests.get(url, params=params)
    data = response.json()
    delivery = data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0]
    now = datetime.now()

    if "VehicleActivity" in delivery:
        with open(FILE, "a", newline="") as f:
            writer = csv.writer(f)
            for vehicle in delivery["VehicleActivity"]:
                journey = vehicle["MonitoredVehicleJourney"]
                call = journey.get("MonitoredCall", {})
                location = journey.get("VehicleLocation", {})
                distances = call.get("Extensions", {}).get("Distances", {})

                row = [
                    now,
                    vehicle.get("RecordedAtTime"),
                    journey.get("VehicleRef"),
                    journey.get("DirectionRef"),
                    location.get("Latitude"),
                    location.get("Longitude"),
                    call.get("StopPointRef"),
                    call.get("StopPointName"),
                    distances.get("DistanceFromCall"),
                    distances.get("StopsFromCall"),
                    call.get("ExpectedArrivalTime"),
                    distances.get("PresentableDistance"),
                ]
                writer.writerow(row)
                print(row[2], row[3], row[7], row[8], "m")
    else:
        print("No buses currently running on Q18 service.")

    print("Waiting 60 seconds")
    time.sleep(60)
