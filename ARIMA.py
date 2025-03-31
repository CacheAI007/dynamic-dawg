import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# Generate a synthetic time series (e.g., sales data)
np.random.seed(42)
n = 100
time_series = np.cumsum(np.random.randn(n))  # Random walk process

# Convert to pandas series
dates = pd.date_range(start="2020-01-01", periods=n, freq="D")
data = pd.Series(time_series, index=dates)

# Step 1: Check for stationarity using Augmented Dickey-Fuller Test
def check_stationarity(series):
    result = adfuller(series)
    print(f'ADF Statistic: {result[0]}')
    print(f'p-value: {result[1]}')
    if result[1] < 0.05:
        print("The series is stationary.")
    else:
        print("The series is not stationary. Differencing is needed.")

check_stationarity(data)

# Step 2: Apply differencing if necessary
diff_data = data.diff().dropna()  # First-order differencing
check_stationarity(diff_data)

# Step 3: Fit ARIMA Model (p=2, d=1, q=2)
model = ARIMA(data, order=(2,1,2))
model_fit = model.fit()

# Step 4: Forecast future values
forecast_steps = 10
forecast = model_fit.forecast(steps=forecast_steps)

# Step 5: Plot the results
plt.figure(figsize=(10,5))
plt.plot(data, label="Actual Data")
plt.plot(pd.date_range(data.index[-1], periods=forecast_steps+1, freq='D')[1:], forecast, label="Forecast", linestyle='dashed', color='red')
plt.legend()
plt.title("ARIMA Time Series Forecast")
plt.show()
