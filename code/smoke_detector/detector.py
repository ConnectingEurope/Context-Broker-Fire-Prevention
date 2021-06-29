import time
import datetime
import os
import shutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 

from local_binary_patterns.lbp_prediction import predict_image
from rule_engine.rule_engine import create_publish_alert_smoke
import rule_engine.rules.rules as rules
import core.fireforest_status_smoke as smoke
import utils.generate_information as generate
import config.config as cnf
config = cnf.Config()

WATCH_FOLDER_PATH = config.watch_folder_path_smoke
RECEIVE_FOLDER_PATH = config.receive_folder_path_smoke
DETECTED_IMAGE_FOLDER_PATH = config.smoke_detected_folder_path
DELTED_IMAGE_FOLDER_PATH = config.deleted_image_folder_path_smoke

SMOKE_SERVICE = config.fireforest_status_smoke
SMOKE_CLASS_NAME = config.smoke_class_name_model
SMOKE_CATEGORY = config.smoke_detector_category
SMOKE_SUBCATEGORY = config.smoke_detector_subcategory
SMOKE_SEVERITY = config.smoke_detector_severity
SMOKE_ID_PROVIDER = config.sensor_info["003"]["id"]

class OnMyWatch:     
    def __init__(self, watch_directory):
        self.watchDirectory = watch_directory
        self.observer = Observer()

    # function to start the listener
    def run(self): 
        event_handler = Handler() 
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True) 
        self.observer.start() 
        print("Waiting for new images...") 
        print("===========================")

        try: 
            while True:
                string_datetime_now, date_datetime_now = generate.datetime_time_tz()
                current_year = date_datetime_now.strftime("%Y")
                current_month = date_datetime_now.strftime("%m")
                current_day = date_datetime_now.strftime("%d")

                receive_folder = "{0}/{1}/{2}/{3}".format(RECEIVE_FOLDER_PATH, current_year, current_month, current_day) 
                
                if os.path.isdir(receive_folder):
                    for file in os.listdir(receive_folder):
                        if file.endswith(".jpg"):
                            full_receive_image_path = os.path.join(receive_folder, file)
                            full_watch_image_path = os.path.join(WATCH_FOLDER_PATH, file)
                            shutil.move(full_receive_image_path, full_watch_image_path)
                            print("{0} - Moved: {1}".format(string_datetime_now, full_watch_image_path))
                    
                time.sleep(5)
        except Exception as ex:
            self.observer.stop() 
            error_text = "Observer stopped. Exception {0}".format(ex)
            print(error_text)
        
        self.observer.join() 
  
class Handler(FileSystemEventHandler): 
    #classify and trigger alert when a new image is added
    @staticmethod
    def on_any_event(event): 
        if event.is_directory: 
            return None
  
        elif event.event_type == 'created':
            image_path = ''

            try:
                # Event is created, you can process it now 
                #print("A new immages has been added: - % s." % event.src_path) 
                print("A new image has been added.") 
                print("Classifying image...") 
                print("===========================")

                #sleep a few seconds to avoid permission errors
                time.sleep(4)
                
                #predict the new image
                image_path = str(event.src_path)
                print("Processing: {0}".format(image_path))
                predict_result, confidence = predict_image(image_path)
                print(predict_result)
                print(confidence)

                string_now_tz, datetime_now_no_micro = generate.datetime_time_tz()

                #Publish smoke detector to orion
                response = smoke.execute_fire_forest_status_smoke(SMOKE_SERVICE, datetime_now_no_micro, predict_result, confidence)
                print("Respose result: {0}".format(response))

                #Generate alert notification
                if (predict_result == SMOKE_CLASS_NAME):
                    attribute = 'smokeDetected'
                    result_prediction = 'True'
                    operator = 'equal'

                    data_rule = {}
                    data_rule["attribute"] = attribute
                    data_rule["dataProvider"] = {"value": SMOKE_ID_PROVIDER}
                    data_rule["dateObserved"] = {"value": {"type": "DateTime", "value": string_now_tz}}
                    data_rule["value"] = result_prediction

                    rule = rules.Rule('', SMOKE_SERVICE, 'FireForestStatus', attribute, operator, result_prediction, SMOKE_CATEGORY, SMOKE_SUBCATEGORY, SMOKE_SEVERITY, '', 0)
                    
                    response = create_publish_alert_smoke(SMOKE_SERVICE, rule, data_rule, image_path)
                    print("Respose result: {0}".format(response))

                    shutil.move(image_path, DETECTED_IMAGE_FOLDER_PATH)
                    print("Smoke images saved: {0} -> {1}".format(image_path, DETECTED_IMAGE_FOLDER_PATH))
                else:
                    shutil.move(image_path, DELTED_IMAGE_FOLDER_PATH)
                    print("Image deleted/moved: {0} -> {1}".format(image_path, DELTED_IMAGE_FOLDER_PATH))

                print("Waiting for new images...") 
                print("===========================")
            except Exception as ex:
                error_text = "Error processing: {0}. Exception {1}".format(image_path, ex)
                print(error_text)

                list_image_name = image_path.split('/')
                image_name_format = list_image_name[len(list_image_name)-1]
                img_name = image_name_format.split('.')[0].replace(" ","_") + "_corrupted"
                img_format = image_name_format.split('.')
                destination_path = os.path.join(DELTED_IMAGE_FOLDER_PATH, img_name) + "." + img_format[len(img_format)-1]

                print("Image deleted/moved: {0} -> {1}".format(image_path, destination_path))
                shutil.move(image_path, destination_path)

            time.sleep(10)

if __name__ == '__main__': 
	print("main")
	watch = OnMyWatch(WATCH_FOLDER_PATH) 
	watch.run() 
