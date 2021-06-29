import pytz
import time
import datetime
import core.airquality_observed_co2 as aqco
import core.airquality_observed_temp_hum as aqth
import core.airquality_observed_wind as aqw

def generate_co2_historical_data():
    datetime_spain = pytz.timezone("Europe/Madrid")
    datetime_now = datetime.datetime.now(datetime_spain)
    datetime_now_no_micro = datetime_now.replace(microsecond=0)
    initial_datetime = datetime_now_no_micro - datetime.timedelta(hours=7*24, minutes=0)
    service_name = 'airqualityobservedco2'
    print(service_name)

    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        aqco.execute_airquality_observed_co2(service_name, initial_datetime)
        initial_datetime = initial_datetime + datetime.timedelta(hours=0, minutes=30)
        time.sleep(0.1)
    
def generate_temp_wind_historical_data():
    datetime_spain = pytz.timezone("Europe/Madrid")
    datetime_now = datetime.datetime.now(datetime_spain)
    datetime_now_no_micro = datetime_now.replace(microsecond=0)
    initial_datetime = datetime_now_no_micro - datetime.timedelta(hours=7*24, minutes=0)
    service_name_1 = 'airqualityobservedtemphum'
    service_name_2 = 'airqualityobservedwind'
    print(service_name_1)
    print(service_name_2)

    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        aqth.execute_airquality_observed_temp(service_name_1, initial_datetime)
        time.sleep(0.1)
        aqw.execute_airquality_observed_wind(service_name_2, initial_datetime)
        time.sleep(0.1)
        initial_datetime = initial_datetime + datetime.timedelta(hours=0, minutes=30)

if __name__ == "__main__":    
    generate_temp_wind_historical_data()
    generate_co2_historical_data()
