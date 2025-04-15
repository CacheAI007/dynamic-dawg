import pandas as pd
import subprocess
file_name = "sorted_storage_unit_price_summary.csv"
df = pd.read_csv(file_name, header=0)  # Read with headers
def competeprice():# Load the CSV file
    # Ensure the second price column (Price2) is numeric
    df.iloc[:, 2] = pd.to_numeric(df.iloc[:, 2], errors='coerce')

    # Function to calculate area from size string
    def get_area(size_str):
        try:
            # Remove " Unit" and split by ' x ' to get dimensions
            size_str = size_str.replace(" Unit", "")
            width, height = map(int, size_str.replace("'", "").split(" x "))
            return width * height
        except ValueError:
            return float('inf')  # Handle invalid formats

    # Create a dictionary of unit sizes and their areas
    unit_areas = {row["Size"]: get_area(row["Size"]) for _, row in df.iterrows()}

    # Get user input
    user_input = input("Enter the storage unit size (e.g., 3x4): ").strip().replace("'", "").replace(" ", "x")

    # Compute the area of the requested size
    try:
        user_width, user_height = map(int, user_input.split("x"))
        user_area = user_width * user_height
        user_size_formatted = f"{user_width}' x {user_height}' Unit"  # Format for exact match
    except ValueError:
        print("Invalid input format. Please use WxH (e.g., 3x4).")
        exit()

    # Check if exact size exists
    if user_size_formatted in unit_areas:
        closest_size = user_size_formatted
    else:
        # If no exact match, find the closest unit by area
        closest_size = min(unit_areas, key=lambda size: abs(unit_areas[size] - user_area))

    # Get the price from the second column (Price2)
    closest_unit_price = df[df["Size"] == closest_size].iloc[:, 2].values[0]

    # Debugging: Show calculated areas and closest match
    #print(f"\nUser input area: {user_area}")
    #print(f"Unit areas: {unit_areas}")
    #print(f"Closest available unit: {closest_size}")
    print(f"Estimated price (from second column): ${closest_unit_price:.2f}")
    return closest_unit_price