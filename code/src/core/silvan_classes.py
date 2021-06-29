from datetime import datetime

# All classes are defined using the data models

#Class for AirQualityObserved
class AirQualityObserved():
	def __init__(self, id_aqo, region, country, latitude, longitude):
		self.id='AirQualityObserved-{0}-{1}'.format(region, id_aqo)
		self.type='AirQualityObserved'
		self.dateObserved=''
		self.location={'type':'Point', 'coordinates':[longitude,latitude]}
		self.name='{0} Air Quality Observed data.'.format(id_aqo)
		self.description='Air Quality Observed data from the {0} sensor in the {1} region.'.format(id_aqo, region)
		self.address={'addressCountry':country, 'addressLocality':region}
		self.dataProvider=id_aqo
		self.temperature=0.0
		self.relativeHumidity=0.0
		self.precipitation=0.0
		self.co2=0.0
		self.windSpeed=0.0
		self.windDirection=0
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
		
#Class for Anomaly		
class Anomaly():
	def __init__(self):
		self.id=''
		self.type='Anomaly'
		self.detectedBy=''
		self.anomalousProperty=''
		self.dateDetected=''
		self.thresholdBreach=[]
		self.dataProvider=''
		self.source=''
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
		
#Class for FireForestStatus
class FireForestStatusPolygon():
	def __init__(self, id_ffs, region, country, polygon_location):
		self.id='FireForestStatus-{0}-{1}'.format(region, id_ffs)
		self.type='FireForestStatus'
		self.dateObserved=''
		self.location={'type':'Polygon', 'coordinates':[polygon_location]}
		self.name='{0} Air Quality Observed data.'.format(id_ffs)
		self.description='Air Quality Observed data from the {0} sensor in the {1} region.'.format(id_ffs, region)
		self.address={'addressCountry':country, 'addressLocality':region}
		self.dataProvider=id_ffs
		self.smokeDetected=False
		self.smokeDetectedConfidence=0.0
		self.fireDetected=False
		self.fireDetectedConfidence=0.0
		self.fireWeatherIndex=0.0
		self.fireForestDailyRiskIndex=0.0
		self.litterCoverage=0.0
		self.soilTemperature=0.0
		self.soilMoistureVwc=0.0
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
class FireForestStatusPointer():
	def __init__(self, id_ffs, region, country, latitude, longitude):
		self.id='FireForestStatus-{0}-{1}'.format(region, id_ffs)
		self.type='FireForestStatus'
		self.dateObserved=''
		self.location={'type':'Point', 'coordinates':[longitude,latitude]}
		self.name='{0} Air Quality Observed data.'.format(id_ffs)
		self.description='Air Quality Observed data from the {0} sensor in the {1} region.'.format(id_ffs, region)
		self.address={'addressCountry':country, 'addressLocality':region}
		self.dataProvider=id_ffs
		self.smokeDetected=False
		self.smokeDetectedConfidence=0.0
		self.fireDetected=False
		self.fireDetectedConfidence=0.0
		self.fireWeatherIndex=0.0
		self.fireForestDailyRiskIndex=0.0
		self.litterCoverage=0.0
		self.soilTemperature=0.0
		self.soilMoistureVwc=0.0
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
