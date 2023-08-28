from django.shortcuts import render, redirect
import os
from .forms import DataEntryForm
from django.conf import settings
from django.templatetags.static import static
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import csv


import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime, timedelta
import random
import numpy as np

def get_ml_images():
    ml_folder = 'static/images/plots/'  # Path to the "ML" folder

    # Get the absolute path to the "ML" folder
    ml_folder_path = os.path.join(settings.STATIC_ROOT, ml_folder)
    ml_folder_path2 = os.path.join(ml_folder_path, "")
    # Initialize a list to store the image URLs
    image_urls = []

    # Iterate through all files in the "ML" folder
    for filename in os.listdir(ml_folder_path2):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # Generate the URL for each image file
            image_path = os.path.join(ml_folder, filename)
            image_url = static(image_path)
            cimage_url = image_url[7:]
            print(cimage_url)
            image_urls.append(cimage_url)

    return image_urls




def index(request):
    allowed_user = 'alpha'  # Replace with the username of the allowed user

    if request.user.is_authenticated and request.user.username == allowed_user:
        show_link = True
    else:
        show_link = False

    return render(request,'index.html', {'show_link': show_link})

def about(request):
    allowed_user = 'alpha'  # Replace with the username of the allowed user

    if request.user.is_authenticated and request.user.username == allowed_user:
        show_link = True
    else:
        show_link = False

    return render(request,"about.html", {'show_link': show_link})

def data_stats(request):
    allowed_user = 'alpha'  # Replace with the username of the allowed user

    if request.user.is_authenticated and request.user.username == allowed_user:
        show_link = True
    else:
        show_link = False

    return render(request,"data_stats.html", {'show_link': show_link})

def contact(request):
    allowed_user = 'alpha'  # Replace with the username of the allowed user

    if request.user.is_authenticated and request.user.username == allowed_user:
        show_link = True
    else:
        show_link = False

    return render(request,"contact.html", {'show_link': show_link})

def predict(request):
    allowed_user = 'alpha'  # Replace with the username of the allowed user

    if request.user.is_authenticated and request.user.username == allowed_user:
        show_link = True
    else:
        show_link = False
    data_folder = 'ML/'
    ml_folder_path = os.path.join(settings.STATIC_ROOT, data_folder)
    csv_path = os.path.join(data_folder, "dummy_data.csv")

    df = pd.read_csv(csv_path)
    

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

    # Print the future DataFrame with predictions
    print(future_df)
    plt_static = 'static/images/plots'
    plt_folder = os.path.join(settings.STATIC_ROOT, plt_static)

    num_bars = int(len(future_df) / 5)

    # Generate x-axis labels for every 5 days
    x_labels = np.arange(0, num_bars)

    # Calculate the average "kg_predicted" values for every 5 days
    avg_kg_predicted = [future_df.iloc[i * 5 : (i + 1) * 5]["kg_predicted"].mean() for i in range(num_bars)]

    matplotlib.use('Agg')
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

    # Show the plo
    predicted_waste = plt_folder + "/daythirty.png"
    plt.savefig(predicted_waste)
    plt.close()

    data_grouped = df.groupby("Month")["Waste Generated"].mean()
    months = data_grouped.index
    waste_values = data_grouped.values
    plt.bar(months, waste_values)
    plt.xlabel("Month")
    plt.ylabel("Waste Generated")
    plt.title("Average Waste Generated by Month")
    plt.xticks(months)
    each_month = plt_folder + "/each_month.png"
    plt.savefig(each_month)
    plt.close()

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
    kg_per_month = plt_folder + "/kg_per_month.png"
    plt.savefig(kg_per_month)
    plt.close()

    image_path = get_ml_images()

    return render(request,"predict.html", {'image_files': image_path,'show_link': show_link})

def logout_view(request):
    logout(request)
    return redirect('index')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('data')
        else:
            # Invalid credentials, display error message or handle as needed
            pass

    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Additional form fields can be retrieved similarly
        user = User.objects.create_user(username=username, password=password)
        # Additional user profile creation or customization can be done here
        login(request, user)
        return redirect('login')

    return render(request, 'signup.html')

@login_required
def data(request):
    allowed_user = 'alpha'  # Replace with the username of the allowed user

    if request.user.is_authenticated and request.user.username == allowed_user:
        show_link = True
    else:
        show_link = False

    csv_file_path = 'static/ML/dummy_data.csv'  # Update with the actual path to your CSV file

    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    rows_per_page = 25
    page = int(request.GET.get('page', 1))


    # Calculate the start and end indexes for the current page
    start_index = (page - 1) * rows_per_page
    end_index = start_index + rows_per_page

    # Get the rows for the current page
    rows = data[start_index:end_index]

    total_pages = (len(data) + rows_per_page - 1) // rows_per_page
    serial_numbers = [(page) * rows_per_page + i + 1 for i in range(len(rows))]
    combined_rows = [{'serial_number': serial, 'row': data} for serial, data in zip(serial_numbers, rows)]
    context = {
        'serial_numbers' : combined_rows,
        'rows': rows,
        'page': page,
        'total_pages': total_pages,
        'show_link': show_link
    }

    return render(request, 'data.html', context)

def form(request):
    allowed_user = 'alpha'  # Replace with the username of the allowed user

    if request.user.is_authenticated and request.user.username == allowed_user:
        show_link = True
    else:
        show_link = False

    return reader(request,'form.html', {'show_link': show_link})


def update_csv(request):
    allowed_user = 'alpha'  # Replace with the username of the allowed user

    if request.user.is_authenticated and request.user.username == allowed_user:
        show_link = True
    else:
        show_link = False

    if request.method == 'POST':
        form = DataEntryForm(request.POST)
        if form.is_valid():
            # Get the form data
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            kg = form.cleaned_data['kg']
            hours_per_day = form.cleaned_data['hours_per_day']
            waste_generated_percentage = kg / hours_per_day
            population_count = form.cleaned_data['population_count']

            # Convert date and time strings to datetime objects
            date_str = date.strftime('%d-%m-%Y')
            time_str = time.strftime('%H:%M:%S')

            # Append the new data as a new row to the CSV file
            csv_file = os.path.join(settings.STATIC_ROOT, 'ML', 'dummy_data.csv')
            print(csv_file)
            fieldnames = ['Date', 'Time', 'kg', 'Hours Per Day', 'Waste Generated', 'Population']
            # Date,Time,kg,Hours Per Day,Waste Generated,Population
            row = [date, time, kg, hours_per_day, waste_generated_percentage, population_count]

            file_exists = os.path.isfile(csv_file)
            with open(csv_file, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()  # Write header only if the file is new

                writer.writerow(dict(zip(fieldnames, row)))
                messages.success(request, 'Update successful!')
                return redirect('index')   # Redirect to the form page after successful submission
    else:
        form = DataEntryForm()

    return render(request, 'update_csv.html', {'form': form,'show_link': show_link})

def update_success(request):
    allowed_user = 'alpha'  # Replace with the username of the allowed user

    if request.user.is_authenticated and request.user.username == allowed_user:
        show_link = True
    else:
        show_link = False
    return render(request,"index.html", {'show_link': show_link})

# import telebot

# # Create a bot instance
# bot = telebot.TeleBot("5885713384:AAEBknEhj9Hsug1MVDcODKX6DnZkrd-bPX0")
# text = 
# # Handle incoming messages
# @bot.message_handler(func=lambda message: message.chat.id == 5248238656)
# def handle_message(message):
#     text = message.text
#     chat_id = message.chat.id

#     # Process the message
#     print(f"Received message from chat {chat_id}: {text}")

# # Start the bot
# bot.polling()

# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse
# import telebot

# # Create a bot instance
# bot = telebot.TeleBot("5885713384:AAEBknEhj9Hsug1MVDcODKX6DnZkrd-bPX0")

# @csrf_exempt
# def telegram_webhook(request):
#     if request.method == 'POST':
#         # Retrieve the message from the request payload
#         update = telebot.types.Update.de_json(request.body)
#         message = update.message

#         # Process the message
#         process_telegram_message(message)
#         redirect('form')
#     return HttpResponse(status=200)

# def process_telegram_message(message):
#     # Handle the received message here
#     text = message.text
#     chat_id = message.chat.id
#     if chat_id == 5248238656:
#     # Process the message as needed
#         print(f"Received message from chat {chat_id}: {text}")


