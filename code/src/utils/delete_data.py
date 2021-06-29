import config.config as cnf
import connectors.orion_connector_ld as orion

config = cnf.Config()
CB_URI_LD = config.context_broker_uri_ld_local
SUB_URI_LD = config.subscription_uri_ld_local

def delete_data(list_services, dict_types):
    for service_name in list_services:
        headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
        }
        
        print(service_name)
        list_response = orion.delete_data(CB_URI_LD, headers, dict_types[service_name])
        
        for response in list_response:
            print(response.status_code)
            #print(response.content)

        list_response = orion.delete_data_sub(SUB_URI_LD, headers)
        for response in list_response:
            print(response.status_code)
            #print(response.content)       

if __name__ == "__main__":
    dict_types = config.entity_types
    list_services = []

    for key in dict_types:
        list_services.append(key)
	
    #list_services = ["fireforeststatussmoke","fireforeststatusdrytrees"]
    #dict_types = {
    #    "fireforeststatussmoke":"FireForestStatus",
    #    "fireforeststatusdrytrees":"FireForestStatus"
    #}

    delete_data(list_services, dict_types)
