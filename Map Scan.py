import googlemaps
from geopy.geocoders import Nominatim

def get_surrounding_addresses(api_key, location, radius=1000):
    """
    Scan surrounding addresses within a specified radius of a location.

    :param api_key: Google Maps API key
    :param location: Input location (string)
    :param radius: Radius in meters to scan for addresses (default: 1000m)
    :return: List of addresses
    """
    try:
        # Initialize Google Maps client
        gmaps = googlemaps.Client(key=api_key)

        # Geocode the input location to get coordinates
        geolocator = Nominatim(user_agent="geoapiExercises")
        geo_location = geolocator.geocode(location)

        if not geo_location:
            return f"Could not geocode the location: {location}"

        lat, lng = geo_location.latitude, geo_location.longitude

        # Search for places around the coordinates within the specified radius
        places = gmaps.places_nearby(location=(lat, lng), radius=radius)

        # Extract addresses from the places result
        addresses = []
        for place in places.get("results", []):
            address = place.get("vicinity")
            if address:
                addresses.append(address)

        return addresses if addresses else "No addresses found in the specified radius."

    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
if __name__ == "__main__":
    api_key = "YOUR_GOOGLE_MAPS_API_KEY"  # Replace with your API key
    location = input("Enter a location: ")
    radius = int(input("Enter a radius in meters (default 1000): ") or 1000)

    addresses = get_surrounding_addresses(api_key, location, radius)

    if isinstance(addresses, list):
        print("Surrounding addresses:")
        for addr in addresses:
            print(f"- {addr}")
    else:
        print(addresses)
