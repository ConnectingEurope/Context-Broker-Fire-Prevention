import requests 

#Does de first request to get the data url contained at 'data' property in AEMET's open data request 
def request_url(url):
    response = requests.get(url)
    json_response = response.json()
    data_url = json_response['datos']
    
    return data_url

#request data to the proper formatted url and returns the response as a json 
def request_data(formatted_url, source):
    if source=='AEMET':
        data_url = request_url(formatted_url)
    else:
        data_url = formatted_url
    
    response = requests.get(data_url)
    json_response = response.json()
    
    return json_response
