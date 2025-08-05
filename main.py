import json
import urllib.request
import certifi
from datetime import datetime, timedelta

TODAY       =datetime.now()
IN_SIX_DAYS =TODAY + timedelta(days=6)

class WeatherForecast:
    def __init__(self, 
                 location_id, 
                 location_name, 
                 date, 
                 morning_forecast, 
                 afternoon_forecast, 
                 night_forecast, 
                 summary_forecast, 
                 summary_when,      
                 min_temp, 
                 max_temp):
        
        self._location_id          = location_id
        self._location_name        = location_name
        self._date                 = date
        self._morning_forecast     = morning_forecast
        self._afternoon_forecast   = afternoon_forecast
        self._night_forecast       = night_forecast
        self._summary_forecast     = summary_forecast
        self._summary_when         = summary_when
        self._min_temp             = min_temp
        self._max_temp             = max_temp

    @property
    def location_id(self):
        return self._location_id

    @property
    def location_name(self):
        return self._location_name

    @property
    def date(self):
        return self._date

    @property
    def morning_forecast(self):
        return self._morning_forecast

    @property
    def afternoon_forecast(self):
        return self._afternoon_forecast

    @property
    def night_forecast(self):
        return self._night_forecast

    @property
    def summary_forecast(self):
        return self._summary_forecast

    @property
    def summary_when(self):
        return self._summary_when

    @property
    def min_temp(self):
        return self._min_temp

    @property
    def max_temp(self):
        return self._max_temp
    
    def __str__(self):
        return (
            f"Location ID       : {self.location_id}\n"
            f"Location Name     : {self.location_name}\n"
            f"...\n"
            f"Date              : {self.date}\n"
            f"...\n"
            f"Morning Forecast  : {self.morning_forecast}\n"
            f"Afternoon Forecast: {self.afternoon_forecast}\n"
            f"Night Forecast    : {self.night_forecast}\n"
            f"...\n"
            f"Summary Forecast  : {self.summary_forecast}\n"
            f"Summary When      : {self.summary_when}\n"
            f"...\n"
            f"Min Temperature   : {self.min_temp}°C\n"
            f"Max Temperature   : {self.max_temp}°C"
        )

class WeatherForecastDatabase:
    def __init__(self):
        self._weather_forecasts =[]

    @property
    def weather_forecasts(self):
        return self._weather_forecasts

    def get_weather_forecasts(self, address:str):
        my_request        =urllib.request.urlopen(address, cafile=certifi.where())
        data              =my_request.read()
        weather_forecasts =json.loads(data)

        for forecast in weather_forecasts:
            weather_forecast =WeatherForecast(forecast['location']['location_id'],
                                              forecast['location']['location_name'],
                                              forecast['date'],
                                              forecast['morning_forecast'],
                                              forecast['afternoon_forecast'],
                                              forecast['night_forecast'],
                                              forecast['summary_forecast'],
                                              forecast['summary_when'],
                                              forecast['min_temp'],
                                              forecast['max_temp'])
            
            self._weather_forecasts.append(weather_forecast)

    def sort_by_date(self):
        self._weather_forecasts.sort(key =lambda x: x.date)

    def sort_by_location_name(self):
        self._weather_forecasts.sort(key =lambda x: x.location_name)

    def sort_by_max_temperature(self):
        self._weather_forecasts.sort(key =lambda x: x.max_temp, reverse =True) 

    def get_forecast_by_location_name(self, location_name:str):
        return list(filter(lambda x: x.location_name ==location_name, self._weather_forecasts))
    
    def get_forecast_by_date(self, date:str):
        return list(filter(lambda x: x.date ==date, self._weather_forecasts))
    
    def get_forecast_by_date_and_location(self, date:str, location_name:str):
        return list(filter(lambda x: x.date ==date and 
                                    x.location_name ==location_name, 
                           self._weather_forecasts))
    
    def get_all_location_names(self):
        return sorted(list(set((map(lambda x: x.location_name, self._weather_forecasts)))))
    
class WeatherForecastApp:
    def __init__(self, address:str):
        self.weather_db =WeatherForecastDatabase()
        self.weather_db.get_weather_forecasts(address)

        print("\n============================")
        print("MALAYSIA WEATHER FORECASTING")
        print("============================\n")

    def help(self):
        print(
            "commands:\n"
            "*********\n"
            "0. quit\n"
            "1. list weather forecasts by location\n"
            "2. list weather forecasts by date\n"
            "3. list weather forecasts by date and location"
        )

    def list_all_location_names(self):
        all_locations =self.weather_db.get_all_location_names()
        print()
        # print location names in two equal-lengths columns
        for i in range(len(all_locations) // 2):
            print(f"{all_locations[i]:35}{all_locations[i + len(all_locations) // 2]}")

    def print_forecast_by_location_name(self):
        self.list_all_location_names() 
    
        location_name =input("\nlocation: ")
        forecasts =sorted(self.weather_db.get_forecast_by_location_name(location_name), key =lambda x: x.date)

        print()
        if len(forecasts) !=0:
            print(f"Weather Forecasts for {location_name} for the Following Week:")
            for forecast in forecasts:
                str_rep =str(forecast)
                print("-" * 50)
                
                #avoid redundancy of repeating the name of location
                print(str_rep[str_rep.find("Date"): ])
            print("-" * 50)
        else:
            print(f"\'{location_name}\' is not a valid location name")

    def print_forecast_by_date(self):
        print(f"\nenter a date from {TODAY.strftime("%Y-%m-%d")} to {IN_SIX_DAYS.strftime("%Y-%m-%d")}:  ")

        date =input("\ndate: ")
        forecasts =sorted(self.weather_db.get_forecast_by_date(date), key =lambda x: x.location_name)

        print()
        if len(forecasts) !=0:
            print(f"Weather Forecasts for {date} in Malaysia:")
            for forecast in forecasts:
                str_rep =str(forecast)
                print("-" * 50)

                #avoid redundancy of repeating the date
                print(str_rep[str_rep.find("Location") : str_rep.find("Date")] +
                      str_rep[str_rep.find("Morning") : ])
            print("-" * 50)
        else:
            print(f"\'{date}\' is not a valid date")

    def print_forecast_by_date_and_location(self):
        self.list_all_location_names() 
        location_name =input("\nlocation: ")

        print(f"\nenter a date from {TODAY.strftime("%Y-%m-%d")} to {IN_SIX_DAYS.strftime("%Y-%m-%d")}:  ")
        date =input("\ndate: ")

        forecasts =self.weather_db.get_forecast_by_date_and_location(date, location_name)
        print()
        if len(forecasts) !=0:
            print(f"Weather Forecast for {date} in {location_name}, Malaysia:")
            for forecast in forecasts:
                str_rep =str(forecast)
                print("-" * 50)

                #avoid redundancy of repeating the date and name of location
                print(str_rep[str_rep.find("Location ID"): str_rep.find("Location Name")] + "...\n" +
                      str_rep[str_rep.find("Morning"): ])  
            print("-" * 50)
        else:
            print(f"invalid input")

    def execute(self):
        while True:
            self.help()
            command =int(input("\ncommand: "))

            if command ==0:
                print("\nexiting...")
                break

            elif command ==1:
                self.print_forecast_by_location_name()

            elif command ==2:
                self.print_forecast_by_date()

            elif command ==3:
                self.print_forecast_by_date_and_location()

            else:
                print("\ninvalid command")
                continue

            print()
        

if __name__ =="__main__":
    address ="https://api.data.gov.my/weather/forecast/"

    weather_app =WeatherForecastApp(address)
    weather_app.execute()


