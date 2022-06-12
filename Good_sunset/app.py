import streamlit as st
import requests
# from streamlit_lottie import st_lottie
from pydoc import visiblename
from bs4 import BeautifulSoup
from PIL import Image

url = "https://weather.com/weather/today/l/-31.95,115.86?par=google"

result = requests.get(url)

doc = BeautifulSoup(result.text, "html.parser")

today = doc.find("div",{"id": "todayDetails"})

data = today.find("div", {"class": "TodayDetailsCard--detailsContainer--16Hg0"})

temperature_find = data.find("span", {"data-testid": "TemperatureValue"})
temperature_farenheit = (temperature_find.string)[:-1]
if temperature_farenheit == "-":
    temperature_farenheit = 212
temperature = round((int(float(temperature_farenheit)) - 32) *5/9,1)


wind_find = data.find("span", {"data-testid": "Wind"})
wind_mph_find = wind_find.find("svg",{"data-testid":"Icon"})
wind_mph = wind_mph_find.next_sibling.strip()[:-4]
wind = round(int(wind_mph) * 1.60934,1)
wind = round(int(wind/1.852),1)


humidity_find = data.find("span", {"data-testid": "PercentageValue"})
humidity = humidity_find.string[:-1]

pressure_home = data.find("span", {"data-testid": "PressureValue"})
pressure_find = pressure_home.find("svg",{"set": "ui"})
pressure_text = pressure_find.next_sibling.strip()[:-3]

pressure = round(int(float(pressure_text)) / 2.036,1)

visibility_find = data.find("span", {"data-testid": "VisibilityValue"})
visibility_text = visibility_find.string[:-3]
visibility = round(int(visibility_text)*1.60934,1)

conditions = doc.find("div", {"class": "CurrentConditions--primary--2SVPh"})
conditions_find = conditions.find("div", {"data-testid": "wxPhrase"})
conditions = conditions_find.string

def sunset_calculator(humidity,pressure,wind,conditions,temperature):
    humidity_rating = humidity_calc(humidity)
    presure_rating = pressure_calc(pressure)
    wind_rating = wind_calc(wind)
    condition_rating = condition_calc(conditions)
    visibility_rating = visibility_calc(visibility)

    sunset_result = humidity_rating * presure_rating * wind_rating * condition_rating * visibility_rating
    if sunset_result > 0.9:
        correct_image = amazing
        correct_text = amazing_text
    
    elif sunset_result > 0.7:
        correct_image = good
        correct_text = good_text

    elif sunset_result > 0.5:
        correct_image = ok
        correct_text = ok_text
    
    else:
        correct_image = trash
        correct_text = trash_text

    return sunset_result, correct_image,correct_text

def visibility_calc(visibility):
    visibility = int(visibility)
    if visibility < 0.3704:
        return 0
    elif visibility < 3.704:
        return 0.2
    elif visibility < 9.26:
        return 0.9
    else:
        return 1

    ###
def humidity_calc(humidity):
    humidity = int(humidity)
    if humidity >= 30 and humidity <= 70:
        return 1
    elif humidity < 30:
        return 0.5
    elif humidity < 90:
        return 0.5
    else:
        return 0

def pressure_calc(pressure):
    return 1

def wind_calc(wind):
    wind = int(wind)
    if wind <= 10:
        return 1
    elif wind < 20:
        return 0.8
    else:
        return 0.7
    

def condition_calc(conditions):
    thunder = "hunder"
    showers = 'howers'
    rain = 'rain'
    partly = 'artly Cloudy'
    sun = 'unny'
    sunish = 'ostly Sunny'
    if thunder in conditions:
        return 0
    elif rain in conditions:
        return 0
    elif showers in conditions:
        return 0.2
    elif partly in conditions:
        return 1
    elif sun in conditions:
        return 0.6
    elif sunish in conditions:
        return 1
    else:
        return 0.5
    
    
# amazing = Image.open(r'C:\Users\galna\OneDrive\Documents\Good_sunset\amazing.jpg')
# good = Image.open(r'C:\Users\galna\OneDrive\Documents\Good_sunset\good.jpg')
# ok = Image.open(r'C:\Users\galna\OneDrive\Documents\Good_sunset\ok.jpg')
# trash = Image.open(r'C:\Users\galna\OneDrive\Documents\Good_sunset\bad.jpg')

amazing = Image.open(r'sunset\amazing.jpg')
good = Image.open(r'https://github.com/GalNaveh/sunset/blob/main/Good_sunset/good.jpg','rb')
ok = Image.open(r'https://github.com/GalNaveh/sunset/blob/main/Good_sunset/ok.jpg')
trash = Image.open(r'https://github.com/GalNaveh/sunset/blob/main/Good_sunset/bad.jpg')

amazing_text = 'godly sunset incoming'
good_text = "bro its going to be a good one"
ok_text = " bit meh tbh"
trash_text = "trash city population this sunset"


st.set_page_config(page_title="Will it be a good Sunset?", page_icon=":sunny:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

sun_animation = load_lottieurl("https://assets1.lottiefiles.com/private_files/lf30_6gqfjgqh.json")

with st.container():
    st.subheader("Sunset Saviour")
    st.write("[Link to data>](https://weather.com/weather/today/l/-31.95,115.86?par=google)")

with st.container():
    st.write("---")
    left_column,right_column = st.columns(2)
    with left_column:
        st.title("I can tell if it will be a good Sunset")
    with right_column:
        pass
#         st_lottie(sun_animation,height=300, key="coding")


with st.container():
    st.write("---")
    left_column,right_column = st.columns(2)
    with left_column:
        if st.button('Sunset Calculator'):
            sunset_result,correct_image,correct_text = sunset_calculator(humidity,pressure,wind,conditions,temperature)
            st.write("rating =",sunset_result)
            st.write(correct_text)
            with right_column:
                st.image(correct_image)
        else:
            st.write("Click to find out today sunset rating")
 
