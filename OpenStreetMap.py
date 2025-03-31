import requests
import csv

def get_addresses_and_businesses_in_radius(lat, lon, radius):
    """
    Retrieve all registered addresses and business names within a specified radius.

    Parameters:
        lat (float): Latitude of the center point.
        lon (float): Longitude of the center point.
        radius (int): Radius in meters to search.

    Returns:
        list: A list of dictionaries containing business names and addresses.
    """
    # Overpass API URL
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Overpass QL query to fetch nodes with 'name' (business names) and address data
    query = f"""
    [out:json];
    node
      (around:{radius},{lat},{lon})
      ["name"];
    out;
    """

    try:
        # Send the HTTP request to the Overpass API
        response = requests.get(overpass_url, params={'data': query})
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Extract business names and addresses
        results = []
        for element in data.get("elements", []):
            if "tags" in element:
                name = element["tags"].get("name", "Unknown Business")
                housenumber = element["tags"].get("addr:housenumber", "")
                street = element["tags"].get("addr:street", "")
                city = element["tags"].get("addr:city", "")
                postcode = element["tags"].get("addr:postcode", "")

                # Store each entry as a dictionary
                address_data = {
                    "Name": name,
                    "House Number": housenumber,
                    "Street": street,
                    "City": city,
                    "Postcode": postcode
                }

                if address_data not in results:  # Avoid duplicates
                    results.append(address_data)

        return results

    except requests.RequestException as e:
        print(f"Error while fetching data from Overpass API: {e}")
        return []

def save_to_csv(data, filename):
    """
    Save the list of address data to a CSV file.

    Parameters:
        data (list): List of address data dictionaries.
        filename (str): The name of the CSV file to save the data to.
    """
    # Write data to CSV
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Name", "House Number", "Street", "City", "Postcode"])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f"Data has been saved to {filename}")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

# Example Usage
if __name__ == "__main__":
    print("Enter the location details (latitude, longitude):")
    coordinates = input("Coordinates (e.g., 37.7749, -122.4194): ")
    latitude, longitude = [float(coord.strip()) for coord in coordinates.split(',')]
    search_radius = int(input("Search radius (in meters): "))

    print("Fetching addresses and business names...")
    results = get_addresses_and_businesses_in_radius(latitude, longitude, search_radius)

    if results:
        # Save results to CSV file
        save_to_csv(results, "businesses_and_addresses.csv")
    else:
        print("No businesses or addresses found in the specified area.")
