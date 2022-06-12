from pydoc import visiblename
from bs4 import BeautifulSoup
import requests
import pygame

pygame.init()

X = 540
Y = 540

display_surface = pygame.display.set_mode((X, Y))

pygame.display.set_caption('Sunset_predictor')

font = pygame.font.SysFont(None, 40)

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

    # print(humidity_rating,presure_rating,wind_rating,condition_rating,visibility_rating)
    print(sunset_result)

    visual(sunset_result) #use pygame or straight to website?

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

def visual(sunset_results):
    display_surface.fill("white")
    
    

    amazing = pygame.image.load(r'amazing.jpg')
    good = pygame.image.load(r'good.jpg')
    ok = pygame.image.load(r'ok.jpg')
    trash = pygame.image.load(r'bad.jpg')

    amazing_text = 'godly sunset incoming'
    good_text = "bro its going to be a good one"
    ok_text = " bit meh tbh"
    trash_text = "trash city population this sunset"

    if sunset_results > 0.9:
        display_surface.blit(amazing, (0, 0))
        word = font.render(amazing_text, True, "black")
        display_surface.blit(word, (20, Y/3))
    
    elif sunset_results > 0.7:
        display_surface.blit(good, (0, 0))
        word = font.render(good_text, True, "black")
        display_surface.blit(word, (20, Y/3))
        pass

    elif sunset_results > 0.5:
        display_surface.blit(ok, (0, 0))
        word = font.render(ok_text, True, "black")
        display_surface.blit(word, (20, Y/3))
        pass

    else:
        display_surface.blit(trash, (0, 0))
        word = font.render(trash_text, True, "black")
        display_surface.blit(word, (20, Y/3))
        pass

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

sunset_calculator(humidity,pressure,wind,conditions,temperature)