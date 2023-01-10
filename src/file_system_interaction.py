from datetime import datetime, date
import time
import os
from .settings_manager import *
from shutil import rmtree

def generate_folder_and_file_name(settings):
    loc_time = time.localtime()
    folder_name = dict()
    file_name = dict()

    if("with_detailed_output" in settings["work_flow"] and settings["work_flow"]["with_detailed_output"]):
        folder_name["detailed"] = settings["work_flow"]["cwd"] + settings["work_flow"]["folder_detailed_output"] + time.strftime(r""+hard_coded_settings["date_format"],loc_time) + "/"
        file_name["detailed"] = "root_information_" + time.strftime(r""+hard_coded_settings["date_and_time_format"],loc_time) + ".json"

    if("with_finished_jobs_output" in settings["work_flow"] and settings["work_flow"]["with_finished_jobs_output"]):
        folder_name["finished"] = settings["work_flow"]["cwd"] + settings["work_flow"]["folder_finished_jobs"]
        file_name["finished"] = "finished_root_information_" + time.strftime(r""+hard_coded_settings["date_format"],loc_time) + ".json"

    if("with_summary" in settings["work_flow"] and settings["work_flow"]["with_summary"]):
        folder_name["summary"] = settings["work_flow"]["cwd"] + settings["work_flow"]["folder_summary"]
        file_name["summary"] = "summary_" + time.strftime(r""+hard_coded_settings["date_format"],loc_time) + ".json"

    if("with_graphical_output" in settings["work_flow"] and settings["work_flow"]["with_graphical_output"]):
        folder_name["graphs"] = settings["work_flow"]["cwd"] + settings["work_flow"]["folder_graphs"] + time.strftime(r""+hard_coded_settings["date_format"],loc_time) + "/"

    for folder in folder_name.values():
        if(not os.path.exists(folder)):
            os.makedirs(folder)
            
    return folder_name, file_name

def extract_timestamp_from_file_name(file_name):
    if("-checkpoint" in file_name):
        return 0
    old_date_and_time = file_name.rsplit(".",1)[0].rsplit("/")[-1].replace("root_information_","")
    return int(time.mktime(datetime.strptime(old_date_and_time,hard_coded_settings["date_and_time_format"]).timetuple()))

def search_for_old_folders(folder_name):
    base_folder = folder_name["detailed"] + "/.." #os.getcwd() + "/detailed_data/"
    output = list()
    for subdir, dirs, files in os.walk(base_folder):
        for dir in dirs:  
            if(os.path.normpath(subdir + "/" + dir) != os.path.normpath(folder_name["detailed"])):
                output.append(os.path.normpath(subdir + "/" + dir))
    return output

def clean_up_at_new_day(folder_name):
    list_of_folders = search_for_old_folders(folder_name)
    for folder in list_of_folders:
        print("Delete folder {}".format(folder))
        rmtree(folder)

def generate_file_list_of_today(folder_name):
    file_list = list()
    base_folder = folder_name["detailed"] #os.getcwd() + "/detailed_data/"
    for subdir, dirs, files in os.walk(base_folder):
        for file in files:
            total_file_name = subdir + "/" + file
            get_date_of_file = date.fromtimestamp(extract_timestamp_from_file_name(total_file_name))
            get_date_of_today = date.today()
            if(get_date_of_file == get_date_of_today):
                file_list.append(os.path.normpath(total_file_name))
    return file_list