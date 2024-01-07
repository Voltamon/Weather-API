import requests
from datetime import datetime
from requests.exceptions import ConnectionError

class WeatherApp():
    def __init__(self):
        self.api_key = ["JDGnXhCOCIafqb5UOU0mkdgVbwAVDijD", "OTda2yqDln959PLbDdyrvgwduCpSYNgK", "l5p35qukE5crJlIvvL2tFJlTthp9dvaY"]
        self.i = 0
  
    def get_city_id(self, city_name):
        try:
          url = f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=%09{self.api_key[self.i]}&q={city_name}&language=en-us&details=true'

          req = requests.get(url)
          data = req.json()
          id = data[0]["Key"]

          return id
        except KeyError:
          if not self.i == 2:
            self.i += 1
            return self.get_city_id(city_name)
          else:
            print("Limit reached for the day")
            exit()      
    
    def get_current_data(self, city_name):
        try:
          city_key = self.get_city_id(city_name)

          url = f'http://dataservice.accuweather.com/currentconditions/v1/{city_key}?apikey={self.api_key[self.i]}&language=en-us&details=true'

          req = requests.get(url)
          data = req.json()

          return data[0]
        except KeyError:
          if not self.i == 2:
            self.i += 1
            return self.get_current_data(city_name)
          else:
            print("Limit reached for the day")
            exit()
  
    def get_forecast_data(self, city_name):
        try:
          city_key = self.get_city_id(city_name)

          url = f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{city_key}?apikey={self.api_key[self.i]}&language=en-us&details=false&metric=true'

          req = requests.get(url)
          data    = req.json()

          return data["DailyForecasts"]
        except KeyError:
          if not self.i == 2:
            self.i += 1
            return self.get_forecast_data(city_name)
          else:
            print('Limit reached for the day')
            exit()
            
    def current_weather(self, city_name):
        weather_data = self.get_current_data(city_name)
        
        wt_city_name = city_name
        wt_status = weather_data["WeatherText"] 
        
        wt_temp_val = str(weather_data["Temperature"]["Metric"]["Value"])
        wt_temp_rf = str(weather_data["RealFeelTemperature"]["Metric"]["Value"])
        wt_temp_phrase = weather_data["RealFeelTemperature"]["Metric"]["Phrase"]
        
        wt_pres_val = str(int(weather_data["Pressure"]["Metric"]["Value"]))
        wt_pres_desc = weather_data["PressureTendency"]["LocalizedText"]
        
        wt_humidity = str(weather_data["RelativeHumidity"])
                
        wt_wind_spd = str(weather_data["Wind"]["Speed"]["Metric"]["Value"])
        wt_wind_gst = str(weather_data["WindGust"]["Speed"]["Metric"]["Value"])
        wt_wind_dir = weather_data["Wind"]["Direction"]["English"]
        
        print(f'{wt_city_name[0:12]}', f'{wt_status[0:15]}', sep=str(" " * (40 - len(wt_city_name[0:12] + wt_status[0:15]))))
        print(f'{wt_temp_phrase} {wt_temp_val}°C', f'(Feels like {wt_temp_rf}°C)', sep=str(" " * (40 - len(wt_temp_phrase) - 26)))
        print(f'{wt_pres_desc[0:8]} {wt_pres_val} hpa', f'Humidity {wt_humidity}%', sep=str(" " * (40 - len(wt_pres_desc[0:8] + wt_pres_val + wt_humidity) - 15)))
        print(f'{wt_wind_spd} km/h from {wt_wind_dir}', f'Gust {wt_wind_gst} km/h', sep=str(" " * (40 - len(wt_wind_spd + wt_wind_dir + wt_wind_gst) - 21)))
        print()

    def forecast_weather(self, city_name):
        weather_data = self.get_forecast_data(city_name)
        
        for i in range(0, 5):
            data = weather_data[i]
            
            date = str(data["Date"][0:10])
            wt_date = datetime.strptime(date, "%Y-%m-%d")
            wt_date = str(wt_date.strftime("%B %d"))
            
            wt_temp_min = str(data["Temperature"]["Minimum"]["Value"])
            wt_temp_max = str(data["Temperature"]["Maximum"]["Value"])
            
            wt_desc = str(data["Day"]["IconPhrase"])
            wt_desc = wt_desc.replace(" sunshine", "")
            
            print(f'{wt_date}', f'{wt_temp_max}/{wt_temp_min}°C        {wt_desc}', sep=str(" " * (18 - len(wt_date))))
        print()

    def display_menu(self):
        print("    ~~Weather App~~~    ")
        print()
        print("1> See Current Weather")
        print("2> Check 5-day forecast")
        print("3> Search for another city")
        print("4> Exit")
        print()

    def main(self):
        city_name = input("Enter city name : ")
        print()

        while True:
            self.display_menu()

            try:
                ch = int(input("Enter your choice : "))
                print()

                if ch == 1:      
                    self.current_weather(city_name)
                elif ch == 2:        
                    self.forecast_weather(city_name)
                elif ch == 3:
                    self.main()
                elif ch == 4:
                    exit()
                else:
                    raise ValueError
            except IndexError:
                print("City doesn't exist, Try Again")
                print()
                self.main()
            except ValueError:
                print("Invalid Input, Try Again")
                print()
            except ConnectionError:
                print("Check your internet connection, Try Again")
                print()

if __name__ == "__main__":
    WeatherApp().main()