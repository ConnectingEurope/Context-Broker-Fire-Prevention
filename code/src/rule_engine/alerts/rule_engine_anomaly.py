class Anomaly_ld():
    def __init__(self, id, anomalousProperty, detectedBy, dateDetected):
        self.id = id
        self.detectedBy = detectedBy
        self.dateDetected = dateDetected
        self.thresholdBreach = []

    def update_dateDetected(self, dateDetected):
        self.dateDetected = dateDetected
    
    def addThresholdBreach(self, dateObserved, measuredValue, thresholdType, thresholdValue):
        threshold = {
            "dateObserved": dateObserved,
            "measuredValue": measuredValue,
            "thresholdType": thresholdType,
            "thresholdValue": thresholdValue
        }
        self.thresholdBreach.append(threshold)
    
    def create_anomaly_json(self):
        anomaly = {
            "id": self.id,
            "type": "Anomaly",
            "detectedBy": self.detectedBy,
            "anomalousProperty": self.anomalousProperty,
            "dateDetected": self.dateDetected,
            "thresholdBreach": self.thresholdBreach,
            "@context": [
                "https://smartdatamodels.org/context.jsonld"
            ]
        }
        
        return anomaly



class Anomaly_v2():
    def __init__(self, id, anomalousProperty, dateDetected, detectedBy):
        self.id = id
        self.anomalousProperty = anomalousProperty
        self.dateDetected = dateDetected
        self.detectedBy = detectedBy
        self.thresholdBreach = []
    
    def update_dateDetected(self, dateDetected):
        self.dateDetected = dateDetected

    def addThresholdBreach(self, dateObserved, value, unitCode,thresholdType, thresholdValue):
        threshold = {
            "datasetId": "Breach{}".format(len(self.thresholdBreach)+1), #"Breach1"
            "value": {
                "dateObserved": {
                    "value": dateObserved,
                },
                "measuredValue": {
                    "value": value,
                    "unitCode": unitCode #"MTR"
                },
                "thresholdType": {
                    "value": thresholdType #"LOWER"
                },
                "thresholdValue": {
                    "value": thresholdValue,
                    "unitCode": unitCode #"MTR"
                }
            } 
        }
        self.thresholdBreach.append(threshold)
    
    def create_anomaly_json(self):
        anomaly = {
            "id": self.id,
            "type": "Anomaly",
            "detectedBy": {
                "type": "",
                "object": self.detectedBy
            },
            "anomalousProperty": {
                "value": self.anomalousProperty
            },
            "dateDetected": {
                "value": self.dateDetected
            },
            "thresholdBreach": self.thresholdBreach
        }
        return anomaly





