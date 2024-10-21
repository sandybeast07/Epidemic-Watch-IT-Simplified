import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to get weather data from OpenWeather API
def get_weather_data(city):
    api_key = '5e6e097546fb8fc0aee014f16b938931'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to get air quality data from WeatherAPI
def get_air_quality_data(city):
    api_key = 'adc70818468a446a89212608242110'
    url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to scrape population density from CityPopulation
def get_population_density():
    url = 'https://www.citypopulation.de/en/nepal/admin/koshi/04__jhapa/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Finding population density
    density_table = soup.find('table', {'class': 'data'})
    rows = density_table.find_all('tr')
    
    population_data = {}
    for row in rows[1:]:
        columns = row.find_all('td')
        if len(columns) > 1:
            district = columns[0].text.strip()
            density = columns[3].text.strip()  # Assuming density is in the 4th column
            population_data[district] = density
    
    return population_data

# Streamlit app
st.title('Air Quality and Weather Data')

city = st.text_input('Enter city name:', 'Jhapa')

if st.button('Get Data'):
    weather_data = get_weather_data(city)
    air_quality_data = get_air_quality_data(city)
    population_density = get_population_density()
    
    # Check and display Weather Data
    st.subheader('Weather Data')
    if weather_data:
        st.write(f"Temperature: {weather_data['main']['temp']} °C")
        st.write(f"Humidity: {weather_data['main']['humidity']}%")
        st.write(f"Precipitation: {air_quality_data['current']['precip_mm']} mm" if air_quality_data else "Precipitation data not available.")
    else:
        st.error("Could not fetch weather data. Please check the city name.")

    # Check and display Air Quality Data
    st.subheader('Air Quality Data')
    if air_quality_data:
        air_quality_index = air_quality_data.get('current', {}).get('air_quality', {}).get('us-epa-index')
        if air_quality_index is not None:
            st.write(f"Air Quality Index: {air_quality_index}")
        else:
            st.error("Air quality index data not available.")
    else:
        st.error("Could not fetch air quality data. Please check the city name.")

    # Display Population Density
    st.subheader('Population Density')
    if city in population_density:
        st.write(f"Population Density in {city}: {population_density[city]} people/km²")
    else:
        st.write("Population density data not available for this city.")
