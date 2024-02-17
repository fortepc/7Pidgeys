import json
from tkinter import filedialog
from tkinter import Tk

def filter_poi(lat, lng, radius, poi_lat, poi_lng):
    from geopy.distance import geodesic
    poi_distance = geodesic((lat, lng), (poi_lat, poi_lng)).meters
    return poi_distance <= radius

def convert_to_geojson():
    root = Tk()
    root.withdraw()

    # Ask user to select input file
    input_file_path = filedialog.askopenfilename(title="Select JSON Input File", filetypes=[("JSON Files", "*.json")])

    if not input_file_path:
        print("No input file selected. Exiting.")
        return

    # Ask user to select output file
    output_file_path = filedialog.asksaveasfilename(title="Save GeoJSON Output File", defaultextension=".geojson", filetypes=[("GeoJSON Files", "*.geojson")])

    if not output_file_path:
        print("No output file selected. Exiting.")
        return

    # Specify position and range
    center_lat, center_lng = 40.707875, -86.099012
    radius = 59633.91

    with open(input_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    features = []
    for key, values in data.items():
        poi_lat, poi_lng = values.get("lat", 0), values.get("lng", 0)
        if filter_poi(center_lat, center_lng, radius, poi_lat, poi_lng):
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [poi_lng, poi_lat]
                },
                "properties": {
                    "name": values.get("name", ""),
                    "mission": values.get("mission", False)
                }
            }
            features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(output_file_path, 'w') as geojson_file:
        json.dump(geojson_data, geojson_file, indent=2)

    print(f"Conversion and filtering successful. GeoJSON saved to: {output_file_path}")

if __name__ == "__main__":
    convert_to_geojson()
