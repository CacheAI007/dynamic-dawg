import numpy as np
from CompetePrice import competeprice
import subprocess

def dynamicdawg(place,unit_size, base_price, occupancy, demand, seasonality, urgency):
    subprocess.run(["python", "Scrape.py",place], check=True)
    subprocess.run(["python", "Extract.py"], check=True)

    def competitive_dynamic_pricing(base_price, occupancy, demand, competitor_price, seasonality, urgency):

        # Weights for each factor
        beta_occupancy = 0.2
        beta_demand = 0.5
        beta_seasonality = 0.4
        beta_urgency = 0.6

        # Calculate an initial dynamic price
        dynamic_price = base_price * (1 +
                                      beta_occupancy * occupancy +
                                      beta_demand * demand +
                                      beta_seasonality * seasonality +
                                      beta_urgency * urgency)

        # Ensure price is within 5-10% of competitor pricing
        min_price = competitor_price * 0.95  # 5% below competitor
        max_price = competitor_price * 1.10  # 10% above competitor

        # Adjust the price to be within competitive range
        competitive_price = np.clip(dynamic_price, min_price, max_price)

        return round(competitive_price, 2)


    # Get user inputs
    #print("Enter values for dynamic pricing calculation:")

    #base_price = float(input("Base Price of Storage Unit: "))
    #occupancy = float(input("Current Occupancy Rate (0 to 1): "))
    #demand = float(input("Demand Factor (0 to 1): "))
    competitor_price = competeprice(unit_size)
    #seasonality = float(input("Seasonality Factor (e.g., 1.2 for peak, 0.8 for off-peak): "))
    #urgency = float(input("Urgency Factor (0 to 1, where 1 is high urgency): "))

    # Calculate competitive dynamic price
    final_price = competitive_dynamic_pricing(base_price, occupancy, demand, competitor_price, seasonality, urgency)

    # Output results
    print(f"\n Suggested Price: ${final_price}")
    return final_price
dynamicdawg("San Bruno, CA","5x5", 55, 0, 0, 0.8, 0)