import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
file_path = "storage_units.csv"  # Update with your actual path
df = pd.read_csv(file_path)

# Clean the data
df = df.drop(columns=['Name', 'Address'], errors='ignore')  # Drop unnecessary columns
df['Price'] = df['Price'].replace('[$,]', '', regex=True).astype(float)  # Convert price to numeric

# Compute mean, median, and mode
summary_stats = df.groupby('Size')['Price'].agg(['mean', 'median', lambda x: x.mode().iloc[0] if not x.mode().empty else None])
summary_stats.columns = ['Mean', 'Median', 'Mode']

# Bar plot for Mean, Median, and Mode
plt.figure(figsize=(10, 6))
summary_stats.plot(kind='bar', figsize=(12, 6))
plt.title('Mean, Median, and Mode of Prices for Each Unit Size')
plt.ylabel('Price ($)')
plt.xlabel('Storage Unit Size')
plt.xticks(rotation=45)
plt.legend(title="Statistics")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Sort by unit size to ensure a logical order
summary_stats_sorted = summary_stats.sort_values(by="Mean")

# Line plot for price changes across unit sizes (Mean Prices)
plt.figure(figsize=(12, 6))
sns.lineplot(x=summary_stats_sorted.index, y=summary_stats_sorted["Mean"], marker="o", linestyle="-", color="b")

# Formatting the plot
plt.title("Price Change Across Unit Sizes (Based on Mean Prices)")
plt.ylabel("Mean Price ($)")
plt.xlabel("Storage Unit Size")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Display the plot
plt.show()

# Display statistics
print(summary_stats)
# Sort by unit size to ensure logical order before saving
summary_stats_sorted = summary_stats.sort_values(by="Mean")

# Save the sorted summary statistics to a CSV file
output_file = "sorted_storage_unit_price_summary.csv"
summary_stats_sorted.to_csv(output_file)

print(f"Sorted summary statistics saved to {output_file}")

