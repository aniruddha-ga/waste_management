import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
import random
import numpy as np
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error, r2_score

# Read the CSV file
df = pd.read_csv("dummy_data.csv")

# Convert date and time values to numerical features
df["Date"] = pd.to_datetime(df["Date"], format='%d-%m-%Y')
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day

df["Time"] = pd.to_datetime(df["Time"],format= '%H:%M:%S')
df["Hour"] = df["Time"].dt.hour
df["Minute"] = df["Time"].dt.minute
df["Second"] = df["Time"].dt.second
df.columns.str.strip()
# Split the data into input (features) and output (target) variables
X = df[["Year", "Month", "Day", "Hour", "Minute", "Second", "Hours Per Day", "Population"]]
y = df[["Waste Generated", "kg"]]

# Train a RandomForestRegressor
model = RandomForestRegressor()
model.fit(X, y)

# Create a new row of data for prediction
# new_data = pd.DataFrame({
#     "Date": ["2023-06-18"],
#     "Time": ["10:00:00"],
#     "kg": [8.5],
#     "Hours Per Day": [8],
#     "Population": [80]
# })


# Get the feature importances from the trained model
importances = model.feature_importances_

# Create a DataFrame to store the feature importances
importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances})

# Sort the DataFrame by importance in descending order
importance_df = importance_df.sort_values('Importance', ascending=False)

# Plot the Feature Importance graph
plt.bar(importance_df['Feature'], importance_df['Importance'])
plt.xticks(rotation='vertical')
plt.xlabel('Features')
plt.ylabel('Importance')
plt.title('Feature Importance')
plt.tight_layout()
plt.savefig("plots/ FI.png")
plt.show()

# Assuming you have true labels and predicted labels
y_true = [0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
y_pred = [0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1]

# Calculate accuracy for different thresholds
thresholds = np.linspace(0, 1, num=100)
accuracies = []

for threshold in thresholds:
    # Convert predicted probabilities to binary predictions based on threshold
    y_pred_binary = [1 if prob >= threshold else 0 for prob in y_pred]

    # Calculate accuracy for the current threshold
    accuracy = accuracy_score(y_true, y_pred_binary)
    accuracies.append(accuracy)

# Plot the accuracy graph
plt.plot(thresholds, accuracies)
plt.xlabel('Threshold')
plt.ylabel('Accuracy')
plt.title('Accuracy vs. Threshold')
plt.grid(True)
plt.savefig("plots/Accuracy.png")
plt.show()





num_future_days = 30

# Get the current date
today = datetime.now().date()

# Generate future dates
future_dates = [today + timedelta(days=i) for i in range(num_future_days)]

# Generate dummy data for the remaining columns
times = [datetime.strptime("{:02d}:{:02d}:{:02d}".format(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)), "%H:%M:%S") for _ in range(num_future_days)]
weights = [random.uniform(5, 10) for _ in range(num_future_days)]
spent_hours = [8.0 if date.weekday() != 5 else 5.0 for date in future_dates]
population = [random.randint(50, 100) for _ in range(num_future_days)]

# Create a DataFrame with the future data
future_df = pd.DataFrame({
    'Year': [date.year for date in future_dates],
    'Month': [date.month for date in future_dates],
    'Day': [date.day for date in future_dates],
    'Hour': [time.hour for time in times],
    'Minute': [time.minute for time in times],
    'Second': [time.second for time in times],
    'kg': weights,
    'Hours Per Day': spent_hours,
    'Population': population
})

# Make predictions using the trained model
future_predictions = model.predict(future_df[["Year", "Month", "Day", "Hour", "Minute", "Second", "Hours Per Day", "Population"]])

# Add the predictions to the future DataFrame
future_df["Waste Generated"] = future_predictions[:, 0]
future_df["kg_predicted"] = future_predictions[:, 1]

plt_t= y[:30]
# Calculate metrics
mse = mean_squared_error(plt_t, future_predictions)
mae = mean_absolute_error(plt_t, future_predictions)
r2 = r2_score(plt_t, future_predictions)

metrics = ['MSE', 'MAE', 'R2']
values = [mse, mae, r2]

# Plot the metrics as a bar chart
plt.bar(metrics, values)
plt.xlabel('Metrics')
plt.ylabel('Value')
plt.title('Model Evaluation Metrics')
plt.savefig("plots/three.png")
plt.show()



# Assume you have a separate DataFrame or series with actual waste generated values for the future dates
actual_waste_generated = pd.Series([random.uniform(5, 10) for _ in range(num_future_days)])

# Calculate the absolute difference between actual and predicted waste generated values
accuracy = abs(future_df["Waste Generated"] - actual_waste_generated)


# Print the future DataFrame with predictions
print(future_df)
num_bars = int(len(future_df) / 5)

# Generate x-axis labels for every 5 days
x_labels = np.arange(0, num_bars)

# Calculate the average "kg_predicted" values for every 5 days
avg_kg_predicted = [future_df.iloc[i * 5 : (i + 1) * 5]["kg_predicted"].mean() for i in range(num_bars)]

# Set the figure size
plt.figure(figsize=(10, 6))

# Plot the bar graph
plt.bar(x_labels, avg_kg_predicted)

# Set the x-axis tick labels to display the combined day ranges
x_tick_labels = [f"{future_df.iloc[i * 5]['Day']} - {future_df.iloc[(i + 1) * 5 - 1]['Day']}" for i in range(num_bars)]
plt.xticks(x_labels, x_tick_labels)

# Set the x-axis label and rotate the x-axis tick labels for better visibility
plt.xlabel('Date Range')
plt.xticks(rotation=45)

# Set the y-axis label
plt.ylabel('kg_predicted')

# Set the title of the graph
plt.title('Predicted kg_predicted for 30 Days (Combined every 5 Days)')

# Show the plot
plt.show()

# Convert date and time values in the new data to numerical features
# new_data["Date"] = pd.to_datetime(new_data["Date"])
# new_data["Year"] = new_data["Date"].dt.year
# new_data["Month"] = new_data["Date"].dt.month
# new_data["Day"] = new_data["Date"].dt.day

# new_data["Time"] = pd.to_datetime(new_data["Time"])
# new_data["Hour"] = new_data["Time"].dt.hour
# new_data["Minute"] = new_data["Time"].dt.minute
# new_data["Second"] = new_data["Time"].dt.second





df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day

# Group the data by month and day and calculate the total kg of waste generated
monthly_weight = df.groupby(['Month', 'Day'])['kg'].sum()

if not os.path.exists('plots'):
    os.makedirs('plots')

# def scatterplot():
#     plt.scatter(df['kg'], df['Waste Generated'], color='blue', label='Generated Data')
#     plt.scatter(new_data['kg'], new_pred[0], color='red', label='Future Prediction')
#     plt.xlabel('Weight (kg)')
#     plt.ylabel('Waste Generated')
#     plt.title('Future Waste Weight Prediction')
#     plt.legend()
#     # Save the scatter plot to a file in the "plots" folder

#     plt.savefig('plots/future_prediction_scatter.png')
#     plt.show()

def barplot():
    data_grouped = df.groupby("Month")["Waste Generated"].mean()
    months = data_grouped.index
    waste_values = data_grouped.values
    plt.bar(months, waste_values)
    plt.xlabel("Month")
    plt.ylabel("Waste Generated")
    plt.title("Average Waste Generated by Month")
    plt.xticks(months)
    plt.savefig('plots/each_month.png')
    plt.show()

def month_plot():
    df['Date'] = pd.to_datetime(df['Date'])

    # Extract the month from the 'date' column
    df['month'] = df['Date'].dt.month

    # Group the data by month and calculate the total kg of waste generated
    waste_per_month = df.groupby('month')['kg'].sum()

    # Create a bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(waste_per_month.index, waste_per_month.values)
    plt.xlabel('Month')
    plt.ylabel('kg of Waste Generated')
    plt.title('kg of Waste Generated per Month')
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.grid(True)
    plt.savefig('plots/kg_per_month.png')
    plt.show()
    


barplot()
month_plot()
# scatterplot()
