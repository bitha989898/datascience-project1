import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


def readCsv():
    dataframe = pd.read_csv('./Postsecondary_School_Locations.csv',
                            encoding='latin')
    dataframe = dataframe.drop(
        columns=['ï»¿X', 'Y', 'FID', 'UNITID', 'STREET', 'ZIP', 'STFIP', 'CNTY', 'LOCALE', 'LAT', 'LON', 'CBSA',
                 'NMCBSA',
                 'CBSATYPE', 'CSA', 'NMCSA', 'NECTA', 'NMNECTA', 'CD', 'SLDL', 'SLDU', 'SCHOOLYEAR', 'STATE'])
    return dataframe


def convertDataframe(df):
    county_state = df.groupby(['NMCNTY'])['NAME'].size().reset_index(
        name="school")
    print(county_state['NMCNTY'].values.tolist())
    print(county_state['school'].values.tolist())
    school_names = county_state['NMCNTY'].values.tolist()
    no_of_schools = county_state['school'].values.tolist()
    barChart(school_names, no_of_schools)


def barChart(school_names, school_list):
    fig = plt.figure(figsize=(25, 10))
    plt.bar(school_names, school_list, align='center', label='Bar Chart')
    plt.xlabel('Schools Names')
    plt.ylabel('No. of schools')
    plt.title('Determine which county has the most school')
    st.pyplot(fig)


def areaChart(df):
    city_state = df.groupby(['CITY'])['NAME'].size().reset_index(
        name="school")
    st.area_chart(city_state)
    st.title("Data")
    st.write(city_state)


def calculate_statistics_for_county(df):
    statistics_dict = dict()
    median = df.groupby(['NMCNTY'])['NAME'].count().median()
    mean = df.groupby(['NMCNTY'])['NAME'].count().mean()
    statistics_dict["median"] = median
    statistics_dict["mean"] = mean
    return statistics_dict


def calculate_statistics_for_city(df):
    statistics_dict = dict()
    median = df.groupby(['CITY'])['NAME'].count().median()
    mean = df.groupby(['CITY'])['NAME'].count().mean()
    statistics_dict["median"] = median
    statistics_dict["mean"] = mean
    return statistics_dict


def streamUI(df):
    firstname = st.text_input("Enter your choice")
    if st.button("Submit"):
        if firstname == 'cities':
            st.header("Showing the area chart")
            areaChart(df)
            estimated_values = calculate_statistics_for_city(df)
            st.write("The Median :", estimated_values["median"])
            st.write("The Mean :", estimated_values["mean"])
        elif firstname == 'county':
            st.header("Showing the bar chart")
            convertDataframe(df)
            estimated_values = calculate_statistics_for_county(df)
            st.write("The Median :", estimated_values["median"])
            st.write("The Mean :", estimated_values["mean"])
        else:
            st.error("Please enter a valid input")


def main():
    st.markdown(
        """
        <style>
        .reportview-container {
            background-color: #222222;
        }
       .sidebar .sidebar-content {
            background: url("https://cdn.hipwallpaper.com/i/80/19/3MoAQj.jpg")
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    dataframe = readCsv()
    streamUI(dataframe)


main()
