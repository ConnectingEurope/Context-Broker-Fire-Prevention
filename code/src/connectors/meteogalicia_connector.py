import connectors.open_data_connector as connector
import config.config as cnf

config = cnf.Config()

API_KEY=config.meteogalicia_api_key
BASE_URI=config.meteogalicia_forecast_uri

# Request meteogalica forecast
def request_meteogalicia_forecast(latitude, longitude):
	source = 'meteogalicia'
	location = '{0},{1}'.format(longitude, latitude)
	uri = BASE_URI + '/getNumericForecastInfo?coords=' + location + '&API_KEY=' + API_KEY
	data = connector.request_data(uri, source)
	return data
