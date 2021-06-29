# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:12:39 2021

@author: edelirio
"""
import os
import re

from rule_engine.rule_engine import create_publish_alert_dry
import rule_engine.rules.rules as rules
import utils.generate_information as generate
import core.fireforest_status_dry as dry_fire_forest
from config import config as cnf
config = cnf.Config()

DRY_SERVICE = config.service_name_dry_detector
DRY_CATEGORY = config.dry_detector_category
DRY_SUBCATEGORY = config.dry_detector_subcategory
DRY_SEVERITY = config.dry_detector_severity
DRY_ID_PROVIDER = config.id_dry_detector
MAX_DRY_PERCENTAGE = config.max_dry_percentage
MAX_FRAME_LIMIT_ALERT = config.max_frame_limit_alert 
DRY_LEAVES_ATTRIBUTE = config.dry_trees_attributte

def process_metadata(metadata_path):
    #metadata_path = r'C:\Users\edelirio\Desktop\CBPilot\mydrytrees\silvan\dry_trees_detector\images\DJI_0053.SRT'
    metadata_path = os.path.splitext(metadata_path)[0]+'.SRT'

    print("Opening file...")
    file = open(metadata_path, "r")
    lines = file.readlines()
    file.close()
    
    temp_metadata = {'frame': [], 'latitude': [], 'longitude': [], 'dateRecorded': [], 'timeRecorded':[]} 
    
    #count = 0
    for line in lines:
        # get frame id
        re_framenumber = re.compile('^[0-9]+$')
        if re_framenumber.search(line):  # re.match() replaced with re.search()
            temp_metadata['frame'].append(line.strip())
            
        # get date recored 2021-05-26 13:59:02,623,871
        re_datetime = re.compile('^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])')
        if re_datetime.search(line): 
            temp_metadata['dateRecorded'].append(line.split(" ")[0].strip())
            
            timeRecorded = line.split(" ")[1].strip()
            temp_metadata['timeRecorded'].append(timeRecorded.split(",")[0])
              
        # get location coordinates
        re_coordinates = re.compile('(\[latitude: (-?[0-9]+.[0-9]+)\]) (\[longtitude: (-?[0-9]+.[0-9]+)\])')

        if re_coordinates.search(line):
            location = re_coordinates.search(line)
            #print(location)
        
            location = re_coordinates.search(line)
            
            latitude = location.group(2)
            longitude = location.group(4)
            
            temp_metadata['latitude'].append(latitude)
            temp_metadata['longitude'].append(longitude)
        
    return temp_metadata
    
def process_percentage_data(data):
    green_percentages = data['greenPixels']
    dry_percentages = data['dryPixels']
    file_names = data["fileName"]
    latitude = data["latitude"]
    print(type(latitude))
    print(latitude)
    longitude = data["longitude"]
    print(type(longitude))
    print(longitude)

    selected_green = []
    selected_dry = []
    
    generated_alert = False
    frames_from_alert = 0
        
    #process the percentages by frame
    for i in range(0, len(green_percentages)):
        green = green_percentages[i]
        dry = dry_percentages[i]
        file_name = file_names[i]
        
        # store the information only for frames with 
        # more than 50% of green and dry pixels detected
        if (green + dry > 50):
            selected_green.append(green)
            selected_dry.append(dry)
              
        # send an alert if the % of dry pixels detected 
        # is more than 40 
        if (dry > MAX_DRY_PERCENTAGE and not generated_alert):
            string_now_tz, datetime_now_no_micro = generate.datetime_time_tz()
                      
            result_value = MAX_DRY_PERCENTAGE/100
            operator = 'higher'

            data_rule = {}
            data_rule["attribute"] = DRY_LEAVES_ATTRIBUTE
            data_rule["dataProvider"] = {"value": DRY_ID_PROVIDER}
            data_rule["dateObserved"] = {"value": {"type": "DateTime", "value": string_now_tz}}
            data_rule["value"] = dry/100 # percentage must be a value between 0 an 1
            data_rule["fileName"] = file_name

            rule = rules.Rule('', DRY_SERVICE, 'FireForestStatus', DRY_LEAVES_ATTRIBUTE, operator, result_value, DRY_CATEGORY, DRY_SUBCATEGORY, DRY_SEVERITY, '', 0)

            response = create_publish_alert_dry(DRY_SERVICE, rule, data_rule)
            
            #the alert is giving response None
            print("Respose result Alert: {0}".format(response))                        
            generated_alert = True
        
        #check that the alert has not been sent in the previous 3 pixels
        if (generated_alert):
            frames_from_alert += 1           
            print('frames from alert: ' + str(frames_from_alert))           
            if frames_from_alert > MAX_FRAME_LIMIT_ALERT:
                generated_alert = False
                frames_from_alert = 0
                
    # process the average % of the whole flight
    try:     
        average_green = sum(selected_green)/len(selected_green)
        average_dry = sum(selected_dry)/len(selected_dry) 
    except:
        print('Average cannot be calculated.')
     

    #post average in Fire Forest Status
    if average_green is not None and average_dry is not None:
        
        average_green = average_green/100
        average_dry = average_dry/100
        dry_detected = False

        if average_dry > MAX_DRY_PERCENTAGE:
            dry_detected = True

        #create fireforest status
        response = dry_fire_forest.execute_fire_forest_status_dry(DRY_SERVICE, datetime_now_no_micro, dry_detected, average_green, average_dry, float(latitude), float(longitude))
        print("Respose result: {0}".format(response))
    else:
        print('No data to publish on CB.')
        
       
    #print(average_dry)

def send_alert_flight_comparison(previous_flight_value, current_flight_value):
    string_now_tz, datetime_now_no_micro = generate.datetime_time_tz()
    
    operator = 'higher'
    data_rule = {}
    data_rule["attribute"] = DRY_LEAVES_ATTRIBUTE
    data_rule["dataProvider"] = {"value": DRY_ID_PROVIDER}
    data_rule["dateObserved"] = {"value": {"type": "DateTime", "value": string_now_tz}}
    data_rule["value"] = current_flight_value/100 # percentage must be a value between 0 an 1
    
    rule = rules.Rule('', DRY_SERVICE, 'FireForestStatus', DRY_LEAVES_ATTRIBUTE, operator, previous_flight_value, DRY_CATEGORY, DRY_SUBCATEGORY, DRY_SEVERITY, '', 0)
    
    response = create_publish_alert(DRY_SERVICE, rule, data_rule)
    
    #the alert is giving response None
    print("Respose result Alert: {0}".format(response))           
        
if __name__ == '__main__': 
    res = {'frame':[1,2,3,4,5,6,7], 'greenPixels':[50,60,90,34, 40, 50, 45], 'dryPixels':[30,20,45,2,40, 50, 45], 'dateRecorded':[1,2,3,4,5,4,5]}
    process_percentage_data(res)
