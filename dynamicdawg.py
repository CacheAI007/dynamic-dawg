import numpy as np
from CompetePrice import competeprice


def competitive_dynamic_pricing(base_price, occupancy, demand, competitor_price, seasonality, urgency):
    """
    Calculates a competitive dynamic price for a storage unit.

    :param base_price: Base price of the storage unit.
    :param occupancy: Current occupancy rate (0 to 1).
    :param demand: Demand factor (0 to 1).
    :param competitor_price: Average competitor pricing.
    :param seasonality: Seasonality factor (e.g., 1.2 for peak, 0.8 for off-peak).
    :param urgency: Urgency factor (0 to 1, where 1 means high urgency).

    :return: Adjusted competitive dynamic price.
    """
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
print("Enter values for dynamic pricing calculation:")

base_price = float(input("Base Price of Storage Unit: "))
occupancy = float(input("Current Occupancy Rate (0 to 1): "))
demand = float(input("Demand Factor (0 to 1): "))
competitor_price = competeprice()
seasonality = float(input("Seasonality Factor (e.g., 1.2 for peak, 0.8 for off-peak): "))
urgency = float(input("Urgency Factor (0 to 1, where 1 is high urgency): "))

# Calculate competitive dynamic price
final_price = competitive_dynamic_pricing(base_price, occupancy, demand, competitor_price, seasonality, urgency)

# Output results
print(f"\n Suggested Price: ${final_price}")