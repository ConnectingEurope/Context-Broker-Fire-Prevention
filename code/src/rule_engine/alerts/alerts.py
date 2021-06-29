#This class contains the structure of the data model ALERT and the needed fields
class Alert():  
	def __init__(self, service_name, alert_field, alert_source, date_issued, category, sub_category, severity, operator, threshold, current_value):
		self.id = "urn:ngsi-ld:Alert:{0}:{1}".format(service_name, alert_field)
		self.type = "Alert"
		self.name = {"type": "Property", "value": alert_field}
		self.description = {"type": "Property", "value": "Alert from service name '{0}'. The parameter '{1}' has been detected with a value of '{2}', it has triggerd the alert because the value is {3} than '{4}'".format(service_name, alert_field, current_value, operator, threshold)}
		self.alertSource = {"type": "Property", "value": alert_source}
		self.category =  {"type": "Property", "value": category}
		self.subCategory = {"type": "Property", "value": sub_category}
		self.severity = {"type": "Property", "value": severity}
		self.dateIssued = {"type": "Property", "value": {"type": "DateTime", "value": date_issued}}

	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

class AlertLdBackup():
  def __init__(self, alertSource, category, createdAt, modifiedAt, dateIssued, description, coordinates, severity,subCategory, validFrom, validTo):
    self.alertSource = alertSource
    self.category = category
    self.createdAt = createdAt
    self.modifiedAt = modifiedAt
    self.dateIssued = dateIssued
    self.description = description
    self.coordinates = coordinates
    self.severity = severity
    self.subCategory = subCategory
    self.validTo = validTo
    self.validFrom = validFrom

  def update_dateModified(self,newDate):
    self.modifiedAt = newDate
  
  def create_alert_json(self, alertID):
    alert = {
      "@context": [
        "https://smartdatamodels.org/context.jsonld",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "alertSource": self.alertSource,
      "category": self.category,
      "createdAt": self.createdAt,
      "dateIssued": {
        "@type": "DateTime",
        "@value": self.dateIssued
      },
      "description": self.description,
      "id": alertID, #"urn:ngsi-ld:Alert:Alert:1"
      "location": {  
        "type": "GeoProperty",  
        "value": {  
            "type": "Point",  
            "coordinates": self.coordinates
        }  
    },  
      "modifiedAt": self.modifiedAt,
      "severity": self.severity,
      "subCategory": self.subCategory,
      "type": "Alert",
      "validFrom": {
        "@type": "DateTime",
        "@value": self.validFrom
      },
      "validTo": {
        "@type": "DateTime",
        "@value": self.validTo
      }
    }
      
    return alert
