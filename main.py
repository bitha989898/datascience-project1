import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


def readCsv():
    dataframe = pd.read_csv('./Postsecondary_School_Locations.csv', encoding='latin')
    dataframe = dataframe.drop(
        columns=['ï»¿X', 'Y', 'FID', 'UNITID', 'STREET', 'ZIP', 'STFIP', 'CNTY', 'LOCALE', 'LAT', 'LON', 'CBSA',
                 'NMCBSA',
                 'CBSATYPE', 'CSA', 'NMCSA', 'NECTA', 'NMNECTA', 'CD', 'SLDL', 'SLDU', 'SCHOOLYEAR', 'STATE'])
    return dataframe


# Function that returns two values
def convertDataframe(df):
    df = pd.DataFrame(df)
    county_state = df.groupby(['NMCNTY'])['NAME'].size().reset_index(
        name="school").sort_values(by='school').nlargest(12, 'school')  # Use of Group by + sort_values + nlargest features of pandas
    school_names = county_state['NMCNTY'].values.tolist()  # Use of Lists
    no_of_schools = county_state['school'].values.tolist()  # Use of Lists
    return school_names, no_of_schools


def barChart(school_names, school_list):
    fig = plt.figure(figsize=(25, 10))
    plt.bar(school_names, school_list, align='center', label='Bar Chart')
    plt.xlabel('County Names')
    plt.ylabel('No. of schools')
    plt.title('Determine which county has the most school')
    st.pyplot(fig)


def areaChart(df, title='Data'):
    city_state = df.groupby(['CITY'])['NAME'].size().reset_index(
        name="school")
    city_state = city_state.sort_values(by='school')  # Use of Sort feature
    st.title(title)
    st.write(city_state)
    city_state = pd.DataFrame(city_state, columns=['school'])
    st.area_chart(city_state)


# function with default parameter and a function that takes at least two parameters and returns a value
def calculate_statistics(df, check='NMCNTY'):
    statistics_dict = dict()
    median = df.groupby([check])['NAME'].count().median()
    mean = df.groupby([check])['NAME'].count().mean()
    statistics_dict["median"] = median
    statistics_dict["mean"] = mean
    return statistics_dict


# Use of Stream Lit UI
def streamUI(df):
    firstname = st.text_input("Enter your choice")
    if st.button("Submit"):
        if firstname == 'cities':
            st.header("Showing the area chart")
            areaChart(df)
            estimated_values = calculate_statistics(df)
            st.write("The Median :", estimated_values["median"])
            st.write("The Mean :", estimated_values["mean"])
        elif firstname == 'county':
            st.header("Showing the bar chart")
            school_names, no_of_schools = convertDataframe(df)
            barChart(school_names, no_of_schools)
            estimated_values = calculate_statistics(df, 'CITY')
            st.write("The Median :", estimated_values["median"])
            st.write("The Mean :", estimated_values["mean"])
        else:
            st.error("Please enter a valid input")


def main():
    # setting the background and side bar image
    st.markdown(
        """
        <style>
        .reportview-container {
            background: #222222;
        }
       .sidebar .sidebar-content {
            background: url("https://cdn.hipwallpaper.com/i/80/19/3MoAQj.jpg")
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Calling the readCSV function
    dataframe = readCsv()
    # Passing the dataframe as a parameter to streamUI function
    streamUI(dataframe)


main()
