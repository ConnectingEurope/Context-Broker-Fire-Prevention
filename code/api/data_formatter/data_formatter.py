import connectors.mysql_connector as mysql
import connectors.orion_connector_ld as orion
import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()

#RULE ENGINE CONSTANTS
RULE_ATTRIBUTE_COLUMN = config.mysql_alert_attribute_column
RULE_ENGINE_TABLE = config.mysql_alert_table
ENTITY_TYPES = config.entity_types
NOTYFY_API_URI = config.api_notify_uri+"notifications"

#This method parse the rule engine dat received from the post
def parse_received_data_rule_engine():
	#Select of the fields of the current rules
	mysql_connector = mysql.connect()
	query = "SELECT {0} FROM {1}".format(RULE_ATTRIBUTE_COLUMN, RULE_ENGINE_TABLE)        
	mysql_result = mysql.select_query(mysql_connector, query)
	
	list_attributes = []
	
	#If there are eisting rules, we add to the list the name of the values to be checked.
	if len(mysql_result) > 0:
		for (attribute,) in mysql_result:
			list_attributes.append(str(attribute))
			
	return list_attributes

#This method creates a dictionary for every rule depending on the received fields.
def data_to_rule_engine(service, dict_data, list_attributes):
	list_data_rules = []
	for attribute in list_attributes:
		if attribute in dict_data:
			data = {"service": service,
					"attribute": attribute,
					"dateObserved": dict_data["dateObserved"],
					"value": dict_data[attribute]["value"],
					"dataProvider" : dict_data["dataProvider"]
					}
			list_data_rules.append(data)
               
	return list_data_rules

#This method transforms a list of tuples with a sigle value [ (value1, ), (value2,), ...] to a list [value1, value2, ...]
def single_value_tuple_list_to_list(tuple_list):
    return [item for t in tuple_list for item in t]

#This method creates a json to be sent to the front end 
def create_rule_json( query_result, column_list ):
    json_result = []
    
    for q in query_result:
        row = {}
        for i in range(len(column_list)):
            row[column_list[i]] = q[i]
        
        json_result.append(row)

    return json_result

#This method extracts the values of a json to create a tuple
def get_rule_values_from_json( json ):
    list_temp = [ json["rule_name"], json["service_name"], json["entity_type"], json["attribute_name"],
    json["operator"], json["threshold"], json["value_category"],json["value_subcategory"], json["value_severity"],
    json["subscription_id"], json["recurrence_seconds"] ]
    tuple_res = []
    for value in list_temp:
        if value == None:
            value = 'NULL'
        tuple_res.append(value)
    return tuple(tuple_res)

#This method creates the string set for an update query for rules
def get_columns_string_for_update( column_tuple ):
    update_set = ""
    aux_tuple = column_tuple[1:]
    for field in aux_tuple:
        if field[0] == "recurrence_seconds" or field[0] == "threshold":
            update_set = update_set + str(field[0])+'=%s,'
        else:
            update_set = update_set + str(field[0])+'="%s",'
    update_set = update_set.rstrip(',')
    return update_set

#This method creates a subscription json
def create_subscription_json( rule_dic ):
	sub_description_alert = "Notify API of {0} {1} {2}".format(rule_dic["attribute_name"], rule_dic["operator"], rule_dic["threshold"])
	list_sub_parameters = ["dateObserved", "dataProvider", rule_dic["attribute_name"]]
	rule_dic["entity_type"]= ENTITY_TYPES[rule_dic["service_name"]]
	if int(rule_dic["recurrence_seconds"]) != 0:
		subs_json = orion.create_json_subscription_alert_condition(sub_description_alert, rule_dic["entity_type"],list_sub_parameters,NOTYFY_API_URI, int(rule_dic["recurrence_seconds"]) )
	else:
		subs_json = orion.create_json_subscription_no_condition(sub_description_alert, rule_dic["entity_type"],list_sub_parameters,NOTYFY_API_URI)
	
	return subs_json

### WEB USERS METHODS ###
#This method check the log in parameters
def login_user(user_data):
    db_connector = mysql.connect()
    query="SELECT * FROM web_users where email='{0}' and password='{1}'".format(user_data['email'], user_data['password'])
    user_info = mysql.select_query(db_connector, query)
    
    if len(user_info) == 0:
        exception_message = "Incorrect user or password"
        raise Exception(exception_message)
    else:
        response = {
            "id"                    : user_info[0][0],
            "username"              : user_info[0][1],
            "email"                 : user_info[0][2],
            "name"                  : user_info[0][4],
        }
        
    return response, 200

#This method registers a user to the mysql
def register_user(user_data):
    db_connector = mysql.connect()
    query="INSERT INTO web_users(username, email, password, name) VALUES('{0}','{1}','{2}','{3}')".format(user_data['username'],user_data['email'], user_data['password'],user_data['name'])
    user_info, code = mysql.insert_query(db_connector, query)

    if not isinstance(user_info, int):
        exception_message = "Missing fields. Fill all the required fields."
        raise Exception(exception_message)
    else:
        response = {
            "id" : user_info
        }

    return response, code
def update_user(user_data):
    db_connector = mysql.connect()
    query="UPDATE web_users SET name='{0}' WHERE id={1}".format(user_data['name'],user_data['id'])
    code = mysql.update_query(db_connector, query)

    if code != 200:
        exception_message = "Could not update. Check updated fields."
        raise Exception(exception_message)
    else:
        response={
            "message" : "user successfully updated."
        }
    return response,code
def delete_user(id):
    db_connector = mysql.connect()
    query="DELETE FROM web_users WHERE id={0}".format(id)
    code = mysql.delete_query(db_connector, query)

    if code != 200:
        exception_message = "Could not delete the user."
        raise Exception(exception_message)
    else:
        response={
            "message" : "user successfully deleted."
        }
    return response,code

def convert_weather_station_data(id_characteristic, characteristic_value):
    characteristic_vr = 0

    if id_characteristic == 1:
        #INT TO HEX
        characteristic_vr_int = int(characteristic_value, 16)

        if characteristic_vr_int > 0x7FFFFFFF:
            negative_value = 0xFFFFFFFF - characteristic_vr_int
            characteristic_vr = (negative_value+1)/1000*(-1)
        else:
            characteristic_vr = int(characteristic_vr_int)/1000
    elif id_characteristic == 5:
        characteristic_vr = int(characteristic_value)/100000
    elif id_characteristic == 15 or id_characteristic == 17 or id_characteristic == 19:
        characteristic_vr = int(characteristic_value)*3.6/1000
    else:
        characteristic_vr = int(characteristic_value)/1000

    return characteristic_vr

def get_characteristic_name(id_characteristic):
    switcher={
        1:"temperature",
        3:"relativeHumidity",
        5:"atmosphericPressure",
        7:"illuminance",
        9:"minWindDirection",
        11:"maxWindDirection",
        13:"windDirection",
        15:"minWindSpeed",
        17:"maxWindSpeed",
        19:"windSpeed",
        21:"precipitation",
        23:"durationPrecipitation",
        25:"intensityPrecipitation",
        27:"maxIntensityPrecipitation"
        }

    return switcher.get(id_characteristic, "")

def format_weather_station(dict_data):
    parsed_dict_data = {}

    device_id = dict_data["ID"]
    string_dateitme, datetime_spain = generate.timepoch_to_datetime(int(dict_data["TS"]))
    id_characteristic = int(dict_data["ST"])

    if id_characteristic == 1:
        characteristic_value = dict_data["VR"]
    else:
        characteristic_value = dict_data["VR"][0]

    characteristic_name = get_characteristic_name(id_characteristic)

    parsed_dict_data["id"] = device_id
    parsed_dict_data[characteristic_name] = convert_weather_station_data(id_characteristic, characteristic_value)
    parsed_dict_data["dateObserved"] = datetime_spain

    return parsed_dict_data