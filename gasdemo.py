from sqlalchemy import create_engine
import streamlit as st
import pandas as pd
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create a connection to your MySQL database
conn = create_engine("mysql://oiviadesu:hidden@0.0.0.0/gas?charset=utf8mb4")

# Write the title to your Streamlit app
st.write("Gas Detector")

# Add a text input field to let users enter the time range
time_range = st.text_input('Enter Time Range', '1min')

# Add a text input field to let users enter the number of latest records
num_records = st.text_input('Enter Number of Latest Records', '100')

# Create a placeholder for the line chart
chart_placeholder = st.empty()

# Create a placeholder for the statistical summary
stats_placeholder = st.empty()

# Create a placeholder for the current status
status_placeholder = st.empty()

# Initialize a variable to keep track of the previous leak status
previous_leak_status = 0

while True:
    # Send a SQL query to your MySQL database and read the result into a pandas DataFrame
    SQL_Query = pd.read_sql('SELECT created_at, id, is_leak, sensor_value FROM gas.gas', conn)

    # Create a new pandas DataFrame from your SQL query result
    df = pd.DataFrame(SQL_Query, columns=['created_at', 'id', 'is_leak', 'sensor_value'])

    # Convert 'created_at' to datetime
    df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S')

    # Set 'created_at' as the index of the DataFrame
    df.set_index('created_at', inplace=True)

    # Limit the DataFrame to the selected number of latest records
    df = df.tail(int(num_records))

    # Resample the DataFrame based on the selected time range
    df_resampled = df.resample(time_range).mean()

    # Update the line chart in your Streamlit app using only the 'sensor_value' column in your DataFrame
    chart_placeholder.line_chart(df_resampled['sensor_value'])

    # Update the statistical summary of the 'sensor_value' column
    stats = df['sensor_value'].describe()
    stats = stats.apply(lambda x: format(x, '.2f'))
    stats_placeholder.write("Statistical Summary of Sensor Values:")
    stats_placeholder.write(stats)

    # Update the current status
    current_status = df.iloc[-1]['is_leak']
    current_sensor_value = df.iloc[-1]['sensor_value']
    status_placeholder.write("Current Status:")
    if current_status == 1:
        status_placeholder.write(f"Gas Detected ({current_sensor_value})")
        if previous_leak_status == 0:
            # Send an email if gas is detected and it was not detected in the previous state
            msg = MIMEMultipart()
            msg['From'] = 'example@icloud.com'  # Sender's email address
            recipients = ['example@swin.edu.au', 'example@pomail.net']  # List of recipients
            msg['To'] = ", ".join(recipients)  # Join the recipients with a comma
            msg['Subject'] = '[Action Required] Gas Detected/Leaking'
            body = f'Halp, Something is leaking since Gas has been detected using MQ2 sensor. The sensor value at the time this mail was sent is {current_sensor_value}. oiviadesu'
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.mail.me.com', 587)  # Gmail's SMTP server
            server.starttls()
            server.login('example@icloud.com', 'hidden')  # Login with your Gmail account
            text = msg.as_string()
            server.sendmail('example@icloud.com', recipients, text)  # Send the email
            server.quit()
    else:
        status_placeholder.write(f"No Gas Detected ({current_sensor_value})")

    # Update the previous leak status
    previous_leak_status = current_status

    # Wait for 3 seconds before the next update
    time.sleep(3)
