from .file_system_interaction import *
import pandas as pd
from datetime import datetime 

def extract_info_of_individual_file_from_summary(file,settings):
    df = pd.read_json(file)
    output = dict()
    output["timestamp"] = extract_timestamp_from_file_name(file)
    output["time"] = datetime.fromtimestamp(output["timestamp"])
    if("cpu_over_time" in settings["summary_output"]):
        output["cpu_over_time"] = df["cpu_percent"].sum()/100.
    if("n_jobs_over_time" in settings["summary_output"]):
        output["n_jobs_over_time"] = len(df)
    if("memory_over_time" in settings["summary_output"]):
        output["memory_over_time"] = df["memory_total"].sum()/1024./1024./1024.
    if("ratio_status_running_over_time" in settings["summary_output"]):
        output["ratio_status_running_over_time"] = len(df[df["status"] == "running"]) /(len(df[df["status"] == "running"]) + len(df[df["status"] == "sleeping"]) + len(df[df["status"] == "disk-sleep"]))
    return output

def generate_summary(folder_name,settings):
    list_of_files = generate_file_list_of_today(folder_name)
    output = list()
    for file in list_of_files:
        output.append(extract_info_of_individual_file_from_summary(file,settings))
    return pd.DataFrame(output)

def write_summary_to_file(summary,folder_name,file_name):
    summary.to_json(folder_name+file_name)
