# All classes are defined using the data models
#Class for AirQualityObserved
class AirQualityObserved():
	def __init__(self, id_aqo, region, country, latitude, longitude):
		self.id="urn:ngsi-ld:AirQualityObserved:{0}:{1}".format(region, id_aqo)
		self.type="AirQualityObserved"
		self.dateObserved={"type": "Property", "value": {"type": "DateTime", "value": ""}}
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": "{0} Air Quality Observed data.".format(id_aqo)}
		self.description={"type": "Property","value": "Air Quality Observed data from the {0} sensor in the {1} region.".format(id_aqo, region)}
		self.address={"type": "Property","value": {"addressCountry":country, "addressLocality":region, "type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_aqo}
		self.temperature={"type": "Property", "value": 0.0}
		self.relativeHumidity={"type": "Property", "value": 0.0}
		self.precipitation={"type": "Property", "value": 0.0}
		self.co2={"type": "Property", "value": 0.0}
		self.windSpeed={"type": "Property", "value": 0.0}
		self.windDirection={"type": "Property", "value": 0}
		self.weatherType={"type": "Property", "value": ""}
		self.atmosphericPressure={"type": "Property", "value": 0.0}
		self.illuminance={"type": "Property", "value": 0.0}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

#Class for AirQualityObserved
class AirQualityObservedGeneral():
	def __init__(self, id_aqo, region, country, name, description, latitude, longitude):
		self.id="urn:ngsi-ld:AirQualityObserved:{0}:{1}".format(region, id_aqo)
		self.type="AirQualityObserved"
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": name}
		self.description={"type": "Property","value": description}
		self.address={"type": "Property","value": {"addressCountry":country, "addressLocality":region, "type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_aqo}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

#Class for GreenspaceRecord
class GreenspaceRecord():
	def __init__(self, id_gsr, region, country, latitude, longitude):
		self.id="urn:ngsi-ld:GreenspaceRecord:{0}:{1}".format(region, id_gsr)
		self.type="GreenspaceRecord"
		self.dateObserved={"type": "Property", "value": {"type": "DateTime", "value": ""}}
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": "{0} GreenspaceRecord data.".format(id_gsr)}
		self.description={"type": "Property","value": "GreenspaceRecord data from the {0} sensor in the {1} region.".format(id_gsr, region)}
		self.address={"type": "Property","value": {"addressCountry":country, "addressLocality":region, "type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_gsr}
		self.soilTemperature={"type": "Property", "value": 0.0}
		self.soilMoistureVwc={"type": "Property", "value": 0.0}
		self.soilMoistureEc={"type": "Property", "value": 0.0}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

#Class for GreenspaceRecord
class GreenspaceRecordGeneral():
	def __init__(self, id_gsr, region, country, name, description, latitude, longitude):
		self.id="urn:ngsi-ld:GreenspaceRecord:{0}:{1}".format(region, id_gsr)
		self.type="GreenspaceRecord"
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": name}
		self.description={"type": "Property","value": description}
		self.address={"type": "Property","value": {"addressCountry":country, "addressLocality":region, "type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_gsr}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

#Class for FireForestStatus
class FireForestStatusPolygon():
	def __init__(self, id_ffs, region, country, polygon_location):
		self.id="urn:ngsi-ld:FireForestStatus:{0}:{1}".format(region, id_ffs)
		self.type="FireForestStatus"
		self.dateObserved={"type": "Property", "value": {"type": "DateTime", "value": ""}}
		self.location={"type": "GeoProperty","value": {"type":"Polygon", "coordinates":[polygon_location]}}
		self.name={"type": "Property","value": "{0} Fire Forest Status data.".format(id_ffs)}
		self.description={"type": "Property","value": "Fire Forest Status data from the {0} sensor in the {1} region.".format(id_ffs, region)}
		self.address={"type": "Property","value": {"addressCountry":country, "addressLocality":region, "type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_ffs}
		self.smokeDetected={"type": "Property","value": False}
		self.smokeDetectedConfidence={"type": "Property","value": 0.0}
		self.dryDetected={"type": "Property","value": False}
		self.greenLeavesDetected={"type": "Property","value": 0.0}
		self.dryLeavesDetected={"type": "Property","value": 0.0}
		self.fireWeatherIndex={"type": "Property","value": 0.0}
		self.dailySeverityRating={"type": "Property", "value": 0.0}
		self.values = {"type": "Property", "value": 0.0}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

#Class for FireForestStatus
class FireForestStatusPolygonGeneral():
	def __init__(self, id_ffs, region, country, name, description, polygon_location):
		self.id="urn:ngsi-ld:FireForestStatus:{0}:{1}".format(region, id_ffs)
		self.type="FireForestStatus"
		self.location={"type": "GeoProperty","value": {"type":"Polygon", "coordinates":[polygon_location]}}
		self.name={"type": "Property", "value": name}
		self.description={"type": "Property","value": description}
		self.address={"type": "Property","value": {"addressCountry":country, "addressLocality":region, "type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_ffs}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

class FireForestStatusPointer():
	def __init__(self, id_ffs, region, country, latitude, longitude):
		self.id="urn:ngsi-ld:FireForestStatus:{0}:{1}".format(region, id_ffs)
		self.type="FireForestStatus"
		self.dateObserved={"type": "Property", "value": {"type": "DateTime", "value": ""}}
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": "{0} Fire Forest Status data.".format(id_ffs)}
		self.description={"type": "Property","value": "Fire Forest Status data from the {0} sensor in the {1} region.".format(id_ffs, region)}
		self.address={"type": "Property","value": {"addressCountry":country, "addressLocality":region, "type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_ffs}
		self.smokeDetected={"type": "Property","value": False}
		self.smokeDetectedConfidence={"type": "Property","value": 0.0}
		self.dryDetected={"type": "Property","value": False}
		self.greenLeaves={"type": "Property","value": 0.0}
		self.dryLeaves={"type": "Property","value": 0.0}
		self.fireWeatherIndex={"type": "Property","value": 0.0}
		self.dailySeverityRating={"type": "Property", "value": 0.0}
		self.values = {"type": "Property", "value": 0.0}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

class FireForestStatusPointerGeneral():
	def __init__(self, id_ffs, region, country, name, description, latitude, longitude):
		self.id="urn:ngsi-ld:FireForestStatus:{0}:{1}".format(region, id_ffs)
		self.type="FireForestStatus"
		self.location={"type": "GeoProperty","value": {"type": "Point", "coordinates": [longitude,latitude]}}
		self.name={"type": "Property","value": name}
		self.description={"type": "Property","value": description}
		self.address={"type": "Property","value": {"addressCountry":country, "addressLocality":region, "type": "PostalAddress"}}
		self.dataProvider={"type": "Property","value": id_ffs}
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
