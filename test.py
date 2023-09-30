import pandas as pd
import streamlit as st

# Specify the full path to your CSV file
csv_file_path = '/Users/manishsaily/Desktop/UNI/Assignment-1/Assignment-task-1/Crash Statistics Victoria.csv'

data = pd.read_csv(csv_file_path)

date_format = '%d/%m/%Y'
data['ACCIDENT_DATE'] = pd.to_datetime(data['ACCIDENT_DATE'], format=date_format)

st.title("Crash Statistics Data Filtering")

# Create a dropdown to select the year
selected_year = st.selectbox("Select a Year", list(range(2013, 2019)))

# Filter rows for the selected year
filtered_data = data[data['ACCIDENT_DATE'].dt.year == selected_year].copy()

# Create a text input for the user to enter an accident type
accident_type = st.text_input("Accident Type:")

# Columns to display in the output
selected_columns = []

if st.button(f"Show Data for {selected_year}"):
    selected_columns = ['OBJECTID', 'ACCIDENT_NO', 'ACCIDENT_STATUS', 'ACCIDENT_DATE', 'ACCIDENT_TIME', 'SEVERITY']
    st.dataframe(filtered_data[selected_columns])


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

#make a button for speed zones
if st.button("speed zones"):
    # Group the data by speed zone and count the number of accidents in each zone
    accident_counts = data['SPEED_ZONE'].value_counts()

    # Create a bar graph to visualize the accident counts per speed zone
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(accident_counts.index, accident_counts.values)

    # Customize the plot
    ax.set_xlabel('SPEED_ZONE')
    ax.set_ylabel('Number of Accidents')
    ax.set_title('Accidents per Speed Zone')
    ax.set_xticks(accident_counts.index)
    ax.set_xticklabels(accident_counts.index, rotation=45)


    # Streamlit app








