import pandas as pd
import streamlit as st

# Specify the full path to your CSV file
csv_file_path = 'C:/Users/manis/PycharmProjects/example/Crash Statistics Victoria.csv'

data = pd.read_csv(csv_file_path)

date_format = '%d/%m/%Y'
data['ACCIDENT_DATE'] = pd.to_datetime(data['ACCIDENT_DATE'], format=date_format)

st.title("Crash Statistics Data Filtering")

# Create a dropdown to select the year
selected_year = st.selectbox("Select a Year", list(range(2015, 2020)))

# Filter rows for the selected year
filtered_data = data[data['ACCIDENT_DATE'].dt.year == selected_year].copy()

# Create a text input for the user to enter an accident type
accident_type = st.text_input("Accident Type:")

# Columns to display in the output
selected_columns = []

if st.button(f"Show Data for {selected_year}"):
    selected_columns = ['OBJECTID', 'ACCIDENT_NO', 'ACCIDENT_STATUS', 'ACCIDENT_DATE', 'ACCIDENT_TIME', 'SEVERITY']
    st.dataframe(selected_year[selected_columns])

# Create a separate button to display data based on the entered accident type
if st.button(f"Show Data for Accident type in {selected_year}"):
    if accident_type:
        filtered_data_type = filtered_data[filtered_data['ACCIDENT_TYPE'].str.contains(accident_type, case=False)]
        selected_columns = ['OBJECTID', 'ACCIDENT_NO', 'ACCIDENT_TYPE', 'ACCIDENT_DATE', 'ACCIDENT_TIME', 'SEVERITY']
        st.dataframe(filtered_data_type[selected_columns])

# Create a button to calculate and display accidents per hour
if st.button("Accidents per hour"):
    time_format = '%H.%M.%S'
    filtered_data['ACCIDENT_TIME'] = pd.to_datetime(filtered_data['ACCIDENT_TIME'], format=time_format)

    # Extract the hour from the "ACCIDENT_TIME" column using .loc
    filtered_data['hour'] = filtered_data['ACCIDENT_TIME'].dt.hour

    # Group the data by hour and count the number of accidents for each hour
    hourly_counts = filtered_data.groupby('hour')['ACCIDENT_TIME'].count()

    # Create a line chart for accidents per hour and label the chart
    chart_data = pd.DataFrame({'Hour': hourly_counts.index, 'Accidents': hourly_counts.values})
    st.line_chart(chart_data.set_index('Hour'))
    st.write("Hourly Accident Counts")
