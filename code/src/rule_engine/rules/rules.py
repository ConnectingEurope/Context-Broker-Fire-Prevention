#This class contains the needed information of the rules
class Rule():
    def __init__(self, rule_id, service_name, entity_type, attribute, operator, threshold, category, sub_category, severity, subscription_id, seconds_to_wait):
        self.id = rule_id
        self.serviceName = service_name
        self.entityType = entity_type
        self.attribute = attribute
        self.operator = operator
        self.threshold = threshold
        self.category = category
        self.subCategory = sub_category
        self.severity = severity
        self.subcsriptionId = subscription_id
        self.secondsToWait = seconds_to_wait

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    #This method evaluates the rule  
    def evaluate(self, external):
        if self.operator == 'greater':
            return external > self.threshold
        elif self.operator == 'lower':
            return external < self.threshold
        elif self.operator == 'equal':
            return self.operator == self.threshold
        else:
            raise ValueError("Operator '{0}' cannot be recognized. Check the value operator inside DB.".format(self.operator))
