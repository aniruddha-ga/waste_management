import pandas as pd
import random
import datetime

# Set the number of dummy data points
num_data_points = 500

# Generate dummy data for the date and time columns
dates = []
times = []
for _ in range(num_data_points):
    # Generate a random date
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2022, 12, 31)
    random_date = start_date + datetime.timedelta(days=random.randint(0, 364))
    dates.append(random_date.strftime('%Y-%m-%d'))

    # Generate a random time
    if random_date.weekday() == 5:  # Saturday
        random_time = datetime.time(random.randint(0, 4), random.randint(0, 59), random.randint(0, 59))
    else:
        random_time = datetime.time(random.randint(0, 7), random.randint(0, 59), random.randint(0, 59))
    times.append(random_time.strftime('%H:%M:%S'))

# Generate dummy data for the kg (weight) column
weights = [random.uniform(5, 10) for _ in range(num_data_points)]

# Generate dummy data for the spent hour per day column
spent_hours = [8.0 if datetime.datetime.strptime(date, '%Y-%m-%d').weekday() != 5 else 5.0 for date in dates]

# Generate dummy data for the waste generated column
waste_generated = [weight / spent_hour for weight, spent_hour in zip(weights, spent_hours)]

# Generate dummy data for the population column
population =  [random.randint(50, 100) for _ in range(num_data_points)]

# Create a DataFrame with the dummy data
df = pd.DataFrame({
    'Date': dates,
    'Time': times,
    'kg': weights,
    'Hours Per Day': spent_hours,
    'Waste Generated': waste_generated,
    'Population': population
})

# Save the DataFrame to a CSV file
df.to_csv('dummy_data.csv', index=False)

# Print a confirmation message
print("Dummy data saved to dummy_data.csv")