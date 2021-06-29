import re
import time
import os
import shutil
import datetime
import pandas as pd
import cv2
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from data_processor.color_detector import detect_color
from data_processor.payload_manager import process_percentage_data, process_metadata, send_alert_flight_comparison
import connectors.mysql_connector as mysql
from config import config as cnf
config = cnf.Config()

WATCH_FOLDER_PATH = config.watch_folder_path_dry 
RECEIVE_FOLDER_PATH = config.receive_folder_path_dry   
RELATIVE_SRT_FOLDER = config.relative_srt_folder # "FOTOS"
DETECTED_IMAGE_FOLDER_PATH = config.dry_detected_folder_path
DELTED_IMAGE_FOLDER_PATH = config.deleted_image_folder_path_dry
CSV_FOLDER = config.dry_process_csv

MILLISECS_PER_FRAME = config.milliseconds_per_frame
MAX_DRY_PERCENTAGE = config.max_dry_percentage
MAX_DIFF_PERCENTAGE = config.max_diff_percentage
DATE_RECORDED_ATTRIBUTE = config.mysql_date_attributte # for SQL queries
DRY_DETECTOR_TABLE = config.mysql_dry_table_name #config.mysql_dry_detector_table

res = {'frame':[], 'greenPixels':[], 'dryPixels':[], 'dateProcessed':[], 'timeProcessed':[], 'fileName':[]}
metadata = {'frame': [], 'latitude': [], 'longitude': [], 'dateRecorded': [], 'timeRecorded':[]} 

def process_video(path):   
    print(path)
    print('-------------------------')
    print("Processing new video...")
    list_video_name = path.split('/')
    video_name_format = list_video_name[len(list_video_name)-1]
    video_name = video_name_format.split('.')[0].replace(" ","_")

    cap = cv2.VideoCapture(path)  #drone_forest_1.mp4
    length_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("Number of frames: {0} // fps: {1}".format(length_frames, fps))

    if length_frames == 0:
        raise Exception("Video is corrupted, no frames detected.")

    print("------------------------------")
    print("Processing metadata...")
    metadata = process_metadata(path)


    previous_now = datetime.datetime.now()
    frames_between_cap = (MILLISECS_PER_FRAME/1000)*fps #1 frame every X seconds = X*fps
    current_frame = 0
    next_frame = 0
    count = 0

    total_steps = length_frames/frames_between_cap
    print("Total steps to process: {0}".format(total_steps))

    while cap.isOpened():
        now = datetime.datetime.now()
        diff = now-previous_now

        time_left = diff*(total_steps-count)
        print("Processing: {0}/{1} -> Time left: {2}".format(count, int(total_steps), time_left))

        cap.set(cv2.CAP_PROP_POS_FRAMES, next_frame)    # extract a frame every X seconds
        ret,frame = cap.read()

        next_frame = current_frame + frames_between_cap

        try:
            aux = detect_color(frame, count)
            res['frame'].append(cap.get(1)) #cap.get(1) gets the current frame number
            res['greenPixels'].append(aux['greenPixels'])
            res['dryPixels'].append(aux['dryPixels'])
            res['dateProcessed'].append(now.strftime("%Y-%m-%d"))
            res['timeProcessed'].append(now.strftime("%H:%M:%S"))

            file_name = '{0}_frame{1}_{2}'.format(video_name, int(next_frame), now.strftime("%Y%m%d_%H%M%S"))
            res["fileName"].append(file_name)

            if aux['dryPixels'] > MAX_DRY_PERCENTAGE:
                print("DRY DETECTED: {0} -> {1} %".format(file_name, aux['dryPixels']))
                cv2.imwrite("{0}/{1}.jpg".format(DETECTED_IMAGE_FOLDER_PATH, file_name), frame)
                #cv2.imwrite(project_root + '/dry_trees_detector/frames/frame%d.jpg' % count, frame)
                #frame_path = project_root + "/dry_trees_detector/frames/frame" + str(count) + "_" + str(now.strftime('%Y-%m-%d')) + ".jpg"
                #cv2.imwrite(frame_path)           
        except Exception as ex:
            if count > total_steps:
                print('Finished processing video.')
            else:
                print('Error processing frame: {0}. Exception: {1}'.format(count, ex))

            break
        finally:
            df_frames = pd.DataFrame.from_dict(res) 
            df_frames['frame'] = df_frames['frame'].astype(int)

        current_frame = next_frame
        previous_now = now
        count += 1

        #it closes the file when the last frame is reached
        if not ret:
            break
            
    cap.release()
    res["latitude"] = metadata["latitude"][0]
    res["longitude"] = metadata["longitude"][0]
    #print(res)
    #process percentages
    print('Processing percentages...')
    process_percentage_data(res)
    print('Done')
        
    # merge metadata with video data
    if metadata != None:
        df_metadata = pd.DataFrame.from_dict(metadata) 
        df_metadata['frame'] = df_metadata['frame'].astype(str).astype(int)
                
        df_final = df_metadata.merge(df_frames, on='frame', how='inner')
        #print(df_final.head())

    #store csv
    csv_name = re.sub(r"[^A-Za-z0-9]", "", str(now))
    df_final.to_csv("{0}/{1}_{2}.csv".format(CSV_FOLDER, video_name, csv_name), index=False)
    
    dictionary_final = df_final.to_dict()
       
    #store in mysql
    print("------------------------------")
    print("Store new data into SQL...")
    mysql_connector = mysql.connect()

    sql_2 = "INSERT INTO " + DRY_DETECTOR_TABLE + " (frame, greenPixels, dryPixels, dateProcessed, timeProcessed,dateRecorded,timeRecorded,lat,lng) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}');"
        
    for i in range(len(res['frame'])):
        sql_final = sql_2.format(dictionary_final['frame'][i], 
                           dictionary_final['greenPixels'][i],  
                           dictionary_final['dryPixels'][i],  
                           dictionary_final['dateProcessed'][i],
                           dictionary_final['timeProcessed'][i],
                           dictionary_final['dateRecorded'][i],
                           dictionary_final['timeRecorded'][i],
                           dictionary_final['latitude'][i],
                           dictionary_final['longitude'][i]
                           
                           )
        
        mysql.insert_query(mysql_connector, sql_final)
        
        
    # compare current flight with previous flight
    #sql_last_trip_date = "SELECT max(dateProcessed) FROM " + DRY_DETECTOR_TABLE + " WHERE dateProcessed != (SELECT max(dateProcessed) FROM " + DRY_DETECTOR_TABLE + ") ;"
     
    sql_last_trip_date = "SELECT max({0}) FROM {1} WHERE {2} != (SELECT max({3}) FROM {4}) ;".format(
            DATE_RECORDED_ATTRIBUTE,
            DRY_DETECTOR_TABLE,
            DATE_RECORDED_ATTRIBUTE,
            DATE_RECORDED_ATTRIBUTE,
            DRY_DETECTOR_TABLE     
            )
    
    print("------------------------------")
    print("Getting data from previous flight...")

    # get most recent date (excluding current date)
    last_date = mysql.select_query(mysql_connector, sql_last_trip_date)
       
    if (last_date[0][0] != None):
        # skip the first time, there is no previous flight        
        # get closest location from previous flight
        sql_3 = '''SELECT dryPixels, lat, lng, ((ACOS(SIN({0} * PI() / 180) *
            SIN(lat * PI() / 180) + COS({1} * PI() / 180) *
            COS(lat * PI() / 180) * COS(({2} - lng) * PI() / 180)) * 180 / PI()) * 60 * 1.1515)
            as distance FROM {3} WHERE '{4}' = '{5}'
            HAVING distance <= 5 ORDER BY distance ASC LIMIT 1 ;'''
            
        for i in range(len(dictionary_final['frame'])):     
            sql_3_final = sql_3.format(
                        dictionary_final['latitude'][i],
                        dictionary_final['latitude'][i],
                        dictionary_final['longitude'][i],
                        DRY_DETECTOR_TABLE, DATE_RECORDED_ATTRIBUTE, last_date[0][0])
                       
            row = mysql.select_query(mysql_connector, sql_3_final)
            
            if row:
                previous_flight_dry = row[0][0]
                
                #current_flight_green = dictionary_final['greenPixels'][i]
                current_flight_dry = dictionary_final['dryPixels'][i]
                
                if (current_flight_dry > previous_flight_dry):
                    diff = current_flight_dry - previous_flight_dry
                    
                    if diff > MAX_DIFF_PERCENTAGE:       
                        print("Higher percentage of dry vegetation detected in current flight.")
                        print(str(current_flight_dry) + " VS " + str(previous_flight_dry))
                        send_alert_flight_comparison(previous_flight_dry, current_flight_dry)
                        
        sql_first_trip_date = "SELECT min( {0} ) FROM {1};".format(DATE_RECORDED_ATTRIBUTE, DRY_DETECTOR_TABLE)
        first_trip_date = mysql.select_query(mysql_connector, sql_first_trip_date)
       
        #delete only if the most recent date (except current flight data) is not the same as the oldest trip
        if (first_trip_date[0][0] != last_date[0][0]):
            print("------------------------------")
            print("Delete old flight data...")
            
            sql_4 = "DELETE FROM {0} WHERE {1} = '{2}';".format(DRY_DETECTOR_TABLE,DATE_RECORDED_ATTRIBUTE,first_trip_date[0][0])
            
            mysql.delete_query(mysql_connector, sql_4)

    #remove current video
    print("-----------------------------")
    print("Removing/Moving source video and metadata...")

    list_video_name = path.split('/')
    video_name = list_video_name[len(list_video_name)-1]
    print(video_name)
    metadata_file_name = video_name.split('.')
    
    shutil.move(path, "{0}/{1}".format(DELTED_IMAGE_FOLDER_PATH, video_name))
    shutil.move(os.path.splitext(path)[0]+'.SRT', "{0}/{1}.SRT".format(DELTED_IMAGE_FOLDER_PATH, metadata_file_name[0]))

    print("Done")

class Handler(PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
       PatternMatchingEventHandler.__init__(
            self,
            patterns=["*.mp4"],
            ignore_directories=True,
            case_sensitive=False,
        )

    def on_any_event(self, event):        
        try:
            size = os.path.getsize(str(event.src_path))
        except FileNotFoundError:
            print("There is no file to process.")
        
        if event.event_type == 'created':
            file_path = str(event.src_path)

            try: 
                print("File created")
                correct_check = 0

                while correct_check < 5:
                    size_0 = os.path.getsize(file_path)
                    time.sleep(5)
                    size_1 = os.path.getsize(file_path)

                    print("Sizes: {0} // {1} // check: {2}".format(size_0, size_1, correct_check))

                    if size_0 == size_1:
                        correct_check +=1
                    else:
                        correct_check = 0
                
                
                print("Processing file {0}".format(file_path))
                process_video(file_path)
            except Exception as ex:
                print('Error processing video: {0}. Exception: {1}'.format(file_path, ex))

                list_video_name = file_path.split('/')
                video_name_format = list_video_name[len(list_video_name)-1]
                video_name = video_name_format.split('.')[0].replace(" ","_") + "_corrupted"
                video_format = video_name_format.split('.')
                destination_path = os.path.join(DELTED_IMAGE_FOLDER_PATH, video_name) + "." + video_format[len(video_format)-1]

                print("Moving video: {0} to {1}".format(file_path, destination_path))
                shutil.move(file_path, destination_path)
            
        #print("[{0}] - [{1}]: [{2}] ".format(time.asctime(), event.event_type, event.src_path))

if __name__ == '__main__':   
        event_handler = Handler()

        observer = Observer()
        observer.schedule(event_handler, WATCH_FOLDER_PATH, recursive=True)
        observer.start()

        try:
            while True:
                #List all files/folders in receive folder
                list_files_folder = os.listdir(RECEIVE_FOLDER_PATH)
                #CHceck every item inside the receive folder
                for item_list in list_files_folder:
                    full_item_path = os.path.join(RECEIVE_FOLDER_PATH, item_list)
                    #Check if the item is a folder
                    if os.path.isdir(full_item_path):
                        #If it isn't the folder home, we can process this folder
                        if item_list != 'home':
                            #print("Process folder: {0}".format(full_item_path))
                            path_sub_folder = os.path.join(full_item_path, RELATIVE_SRT_FOLDER)
                            #Check if a folder inside with name "FOTOS" exists (it must contain .SRT)
                            if os.path.isdir(path_sub_folder):
                                #The SRT folder exists
                                #Try to match MP4 and SRT
                                list_video_files = os.listdir(full_item_path)
                                for video_name_format in list_video_files:
                                    full_file_name_mp4 = os.path.join(full_item_path, video_name_format)
                                    if os.path.isfile(full_file_name_mp4):
                                        video_name = video_name_format.split(".")[0]
                                        #print("video name: {0}".format(video_name))
                                        srt_full_path = os.path.join(path_sub_folder, video_name) + ".SRT"

                                        if os.path.exists(srt_full_path):
                                            #print("GOOD!! The file {0} has SRT file {1}".format(os.path.join(full_item_path, video_name_format), srt_full_path))                                    
                                            watch_folder_tomove_mp4 = os.path.join(WATCH_FOLDER_PATH,video_name+".mp4")
                                            watch_folder_tomove_srt = os.path.join(WATCH_FOLDER_PATH,video_name+".SRT")
                                            print("Moving files:\n{0}\n{1}\nTO: {2}".format(full_file_name_mp4, srt_full_path, WATCH_FOLDER_PATH))
                                            shutil.move(srt_full_path, watch_folder_tomove_srt)
                                            shutil.move(full_file_name_mp4, watch_folder_tomove_mp4)
                                            time.sleep(10)
                                        else:
                                            error = 0
                                            #print("No corresponding SRT file for video: {0} -> {1}".format(os.path.join(full_item_path, video_name_format), srt_full_path))
                                    else:
                                        error = 1
                                        #print("{0} is not a file".format(full_file_name_mp4))
                            else:
                                error = 2
                                #print("There is no folder named '{0}' inside '{1}'".format(RELATIVE_SRT_FOLDER, full_item_path))
                        else:
                            error = 3
                            #print("home directory not used: {0}".format(item_list))
                    else:
                        error = 4
                        #print("item is not a folder: {0}".format(item_list))

                time.sleep(10)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()
        
        
        
        
