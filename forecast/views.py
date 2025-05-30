from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse


import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta

import pytz
import os

API_KEY = 'da3d11cfe2729f3526c5251f2e499679'
BASE_URL = 'https://api.openweathermap.org/data/2.5/'

"""**Fetching Current Weather Data**"""

def get_curr_weather(city):
    try:
       
      url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
      response = requests.get(url)
      data = response.json()


      forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
      forecast_response = requests.get(forecast_url)
      forecast_data = forecast_response.json()
      
      # Extract today's min/max from forecast data
      today = datetime.now().strftime('%Y-%m-%d')
      today_temps = []
      
      for item in forecast_data['list']:
          item_date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
          if item_date == today:
              today_temps.append(item['main']['temp'])
      
      # Calculate real min/max for today
      if today_temps:
          real_temp_min = round(min(today_temps))
          real_temp_max = round(max(today_temps))
      else:
          # Fallback to API values if no forecast data
          real_temp_min = round(data['main']['temp_min'])
          real_temp_max = round(data['main']['temp_max'])
      return {
          'city': data['name'],
          'curr_temp': round(data['main']['temp']),
          'feels_like': round(data['main']['feels_like']),

          'temp_min': real_temp_min,
          'temp_max': real_temp_max,


          'humidity': round(data['main']['humidity']),
          'description': data['weather'][0]['description'],
          'country': data['sys']['country'],
          'wind_gust_dir': data['wind']['deg'],
          'pressure': data['main']['pressure'],
          'wind_gust_speed': data['wind']['speed'],
          'clouds': data['clouds']['all'],
          'visibility': data['visibility'],
          'timezone_offset': data['timezone'],
      }
    except Exception as e:
        print(f"Error fetching weather for city '{city}': {e}")
        return None

"""**Read Weather History**"""

def read_hist_data(filename):
  df = pd.read_csv(filename)
  df = df.dropna()
  df = df.drop_duplicates()
  return df

"""**Preparing Dataset**"""

def prepare_data(data):
  le = LabelEncoder()
  data['WindGustDir'] = le.fit_transform(data['WindGustDir'])
  data['RainTomorrow'] = le.fit_transform(data['RainTomorrow'])

  X = data[['MinTemp','MaxTemp','WindGustDir','WindGustSpeed','Humidity','Pressure','Temp']]
  y = data['RainTomorrow']

  return X, y, le

"""**Training the Model**"""

def train_rain_model(X, y):
  x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  model = RandomForestClassifier(n_estimators=100, random_state=42)
  model.fit(x_train, y_train)

  y_pred = model.predict(x_test)



  print("Mean Squared Error")

  print(mean_squared_error(y_test, y_pred))

  return model

"""**Preparing Dataset for Regression**"""

def prepare_reg_data(data, feature):
  X, y = [], []

  for i in range(len(data)-1):
    X.append(data[feature].iloc[i])
    y.append(data[feature].iloc[i+1])

  X = np.array(X).reshape(-1, 1)
  y = np.array(y)

  return X, y

"""**Training the Regression Model**"""

def train_reg_model(X, y):
  model = RandomForestRegressor(n_estimators=100, random_state=42)
  model.fit(X, y)
  return model

"""**Predicting Future Temperatures and Humidity**"""

def predict_future(model, curr_value):
  predictions = [curr_value]

  for i in range(5):
    next_value = model.predict(np.array([[predictions[-1]]]))
    predictions.append(next_value[0])

  return predictions[1:]

"""**Analyzing the Weather**"""

def weather_view(request):

        if request.method == 'POST':
            city = request.POST.get('city') or 'Kathmandu'

        else:
            city = 'Kathmandu'

        
        curr_weather = get_curr_weather(city)


        err_city = None
        if curr_weather is None:
            err_city = city
            city = 'Kathmandu'
            curr_weather = get_curr_weather(city)






        csv_path = 'askclouds.csv'



        historical_data = read_hist_data(csv_path)









        X, y, le = prepare_data(historical_data)

        rain_model = train_rain_model(X, y)


        wind_deg = curr_weather['wind_gust_dir'] % 360
        compass_points = [
            ("N", 0, 11.25), ("NNE", 11.25, 33.75), ("NE", 33.75, 56.25),
            ("ENE", 56.25, 78.75), ("E", 78.75, 101.25), ("'ESE", 101.25, 123.75),
            ("SE", 123.75, 146.25), ("SSE", 146.25, 168.75), ("S", 168.75, 191.25), ("SSW",191.25, 213.75), ("SW", 213.75, 236.25), ("WSW", 236.25, 258.75), ("W", 258.75, 281.25), ("WNW", 281.25, 303.75), ("NW", 303.75, 326.25),
            ("NNW", 326.25, 348.75)
        ]

        compass_direction = next(
            (point for point, start, end in compass_points if start <= wind_deg < end),
            "N"
        )


        compass_direction_encoded = le.transform([compass_direction])[0] if compass_direction in le.classes_ else -1


        curr_data = {
            'MinTemp': curr_weather['temp_min'],
            'MaxTemp': curr_weather['temp_max'],
            'WindGustDir': compass_direction_encoded,
            'WindGustSpeed': curr_weather['wind_gust_speed'],
            'Humidity': curr_weather['humidity'],
            'Pressure': curr_weather['pressure'],
            'Temp': curr_weather['curr_temp']
        }

        curr_data_df = pd.DataFrame([curr_data])




        rain_prediction = rain_model.predict(curr_data_df)[0]



        x_temp, y_temp = prepare_reg_data(historical_data, 'Temp')
        temp_model = train_reg_model(x_temp, y_temp)

        x_hum, y_hum = prepare_reg_data(historical_data, 'Humidity')
        hum_model = train_reg_model(x_hum, y_hum)


        #predicting future state

        future_temp = predict_future(temp_model, curr_weather['temp_min'])
        future_hum = predict_future(hum_model, curr_weather['humidity'])


        #timing

        ktm_tz = pytz.timezone('Asia/Kathmandu')
        city_time = datetime.now(ktm_tz)



        next_hour = city_time + timedelta(hours=1)
        next_hour = next_hour.replace(minute=0, second=0, microsecond=0)

        future_times = [(next_hour + timedelta(hours=i)).strftime('%H:00') for i in range(5)]













        time1, time2, time3, time4, time5 = future_times
        temp1, temp2, temp3, temp4, temp5 = future_temp
        hum1, hum2, hum3, hum4, hum5 = future_hum



        context = {
            'location': city,
            'current_temp': curr_weather['curr_temp'],
            'feels_like': curr_weather['feels_like'],
            'temp_min': curr_weather['temp_min'],
            'temp_max': curr_weather['temp_max'],
            'humidity': curr_weather['humidity'],
            'clouds': curr_weather['clouds'],
            'description': curr_weather['description'],


            'city': curr_weather['city'],
            'country': curr_weather['country'],


            'time': city_time.now()+timedelta(hours=5, minutes=45),
            'date': (city_time.now()+timedelta(hours=5, minutes=45)).strftime("%B %d, %Y"),

            'wind': curr_weather['wind_gust_speed'],
            'pressure': curr_weather['pressure'],
            'visibility': curr_weather['visibility'],

            'time1': time1,
            'time2': time2,
            'time3': time3,
            'time4': time4,
            'time5': time5,

            'temp1': f"{round(temp1,1)}",
            'temp2': f"{round(temp2,1)}",
            'temp3': f"{round(temp3,1)}",
            'temp4': f"{round(temp4,1)}",
            'temp5': f"{round(temp5,1)}",

            'hum1': f"{round(hum1,1)}",
            'hum2': f"{round(hum2,1)}",
            'hum3': f"{round(hum3,1)}",
            'hum4': f"{round(hum4,1)}",
            'hum5': f"{round(hum5,1)}",
            
            'error': err_city,

        }
        
        return render(request, 'weather.html', context)

                   





