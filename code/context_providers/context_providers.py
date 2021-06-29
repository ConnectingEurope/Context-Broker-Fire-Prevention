import time

import core.airquality_observed_meteogalicia as aqo
import core.fireforest_status_fwi as fwi

import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()

AQI_SERVICE_NAME = config.air_quality_service_meteogalicia
FWI_SERVICE_NAME = config.fireforest_status_fwi
HOUR_TO_PUBLISH = config.hour_to_publish_fwi

if __name__ == "__main__":
    seconds_to_wait = 1*60*60 #1h
    print("START - EXECUTION EVERY {0} seconds.".format(seconds_to_wait))

    while True:
        string_datetime_now, date_datetime_now = generate.datetime_time_tz()

        print("{0} {1}".format(string_datetime_now, AQI_SERVICE_NAME))
        aqo.execute_airquality_observed_meteogalicia(AQI_SERVICE_NAME, date_datetime_now)
        
        if date_datetime_now.hour == HOUR_TO_PUBLISH:
            print("{0} {1}".format(string_datetime_now, FWI_SERVICE_NAME))
            fwi.execute_fire_forest_status_fwi(FWI_SERVICE_NAME, date_datetime_now)

        print("SLEEP {0}".format(seconds_to_wait))
        time.sleep(seconds_to_wait)
