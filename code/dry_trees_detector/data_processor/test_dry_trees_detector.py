#This import is to make the reference properly but with the api you don't need
import os
import shutil
import time

def move_files():
    full_source_path = "/home/ubuntu/silvan/volumes/python/dry_trees_detector/deleted_video/"
    full_destination_path = "/home/ubuntu/silvan/volumes/ftpd/data/RUTA 1 120M/"
    list_video_files = os.listdir(full_source_path)

    for file_name_format in list_video_files:
        file_name = file_name_format.split(".")[0]

        source_mp4_file_path = os.path.join(full_source_path, file_name+".mp4")
        source_srt_file_path = os.path.join(full_source_path, file_name+".SRT")

        destination_mp4_path = os.path.join(full_destination_path, file_name+".mp4")
        destination_srt_path = os.path.join(full_destination_path,"FOTOS", file_name+".SRT")

        shutil.move(source_mp4_file_path, destination_mp4_path)
        shutil.move(source_srt_file_path, destination_srt_path)
        time.sleep(5)
    
    full_source_path = "/home/ubuntu/silvan/volumes/python/dry_trees_detector/watch_folder/"
    full_destination_path = "/home/ubuntu/silvan/volumes/ftpd/data/RUTA 1 120M/"
    list_video_files = os.listdir(full_source_path)

    for file_name_format in list_video_files:
        file_name = file_name_format.split(".")[0]

        source_mp4_file_path = os.path.join(full_source_path, file_name+".mp4")
        source_srt_file_path = os.path.join(full_source_path, file_name+".SRT")

        destination_mp4_path = os.path.join(full_destination_path, file_name+".mp4")
        destination_srt_path = os.path.join(full_destination_path,"FOTOS", file_name+".SRT")

        shutil.move(source_mp4_file_path, destination_mp4_path)
        shutil.move(source_srt_file_path, destination_srt_path)
        time.sleep(5)

if __name__ == "__main__":
    move_files()




