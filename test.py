import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


st.title('Accident Analysis App')
# Upload CSV file
csv_file = st.file_uploader('Upload a CSV file containing accident data', type=['csv'])
if csv_file is not None:
    st.write('CSV file uploaded successfully!')

    data = pd.read_csv(csv_file)

    date_format = '%d/%m/%Y'
    data['ACCIDENT_DATE'] = pd.to_datetime(data['ACCIDENT_DATE'], format=date_format)

    st.title("Crash Statistics Data Filtering")

    # Create a dropdown to select the year
    selected_year = st.selectbox("Select a Year", list(range(2013, 2019)))

    # Filter rows for the selected year
    filtered_data = data[data['ACCIDENT_DATE'].dt.year == selected_year].copy()

    # Create a text input for the user to enter an accident type
    accident_type = st.text_input("Accident Type:")

    # empty list of columns to display the output
    selected_columns = []

    if st.button(f"Show Data for {selected_year}"):
        selected_columns = ['OBJECTID', 'ACCIDENT_NO', 'ACCIDENT_STATUS',
                            'ACCIDENT_DATE', 'ACCIDENT_TIME', 'SEVERITY']
        st.dataframe(filtered_data[selected_columns])

    # Create a separate button to display data based on the entered accident type
    if st.button(f"Show Data for Accident type in {selected_year}"):
        if accident_type:
            filtered_data_type = filtered_data[filtered_data['ACCIDENT_TYPE'].str.contains(accident_type, case=False)]
            selected_columns = ['OBJECTID', 'ACCIDENT_NO', 'ACCIDENT_TYPE',
                                'ACCIDENT_DATE', 'ACCIDENT_TIME', 'SEVERITY']
            st.dataframe(filtered_data_type[selected_columns])

# Create a button to calculate and display accidents per hour
    if st.button("Accidents per hour"):
        time_format = '%H.%M.%S'
        filtered_data['ACCIDENT_TIME'] = pd.to_datetime(filtered_data['ACCIDENT_TIME'], format=time_format)
        filtered_data['hour'] = filtered_data['ACCIDENT_TIME'].dt.hour

        # Group the data by hour and count the number of accidents for each hour
        hourly_counts = filtered_data.groupby('hour')['ACCIDENT_TIME'].count()

        # Create a bar chart for accidents per hour and label the chart
        chart_data = pd.DataFrame({'Hour': hourly_counts.index, 'Accidents': hourly_counts.values})

        fig, ax = plt.subplots()
        ax.bar(chart_data['Hour'], chart_data['Accidents'])
        ax.set_xlabel('Hour')
        ax.set_ylabel('Accidents')
        ax.set_title('Hourly Accident Counts (24h)')
        ax.set_xticks(range(24))
        
        st.pyplot(fig)
        st.write("Hourly Accident Counts")

    # make a button for speed zones
    # Create a button to trigger the analysis
    if st.button("Show data per Speed Zone"):
        # Analyze the data and display the result
        accident_counts = data['SPEED_ZONE'].value_counts().reset_index()
        accident_counts.columns = ['SPEED_ZONE', 'Total Accidents']
        # Display the total accidents per speed zone in a table
        st.write('Total Accidents per Speed Zone:')
        st.write(accident_counts)
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.bar(accident_counts['SPEED_ZONE'], accident_counts['Total Accidents'])
        plt.xlabel('Speed Zone Km/h')
        plt.ylabel('Total Accidents')
        plt.title('Total Accidents per Speed Zone')
        plt.xticks(rotation=40, ha="right")
        st.pyplot(fig)
