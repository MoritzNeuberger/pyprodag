import time
import psutil
import pandas as pd
import numpy as np

one_week = 3600*24*7;

set_of_pids = set()

def check_whether_process_is_of_interest(process,settings):
    output = True

    if("exe" in settings["selection_criteria"]):
        output *= (process.name() == settings["selection_criteria"]["exe"])

    if("status" in settings["selection_criteria"]):
        output *= (process.status() in settings["selection_criteria"]["status"])

    if("user" in settings["selection_criteria"]):
        output *= (process.username() == settings["selection_criteria"]["user"])

    if("users" in settings["selection_criteria"]):
        output *= (process.username() in settings["selection_criteria"]["users"])

    if("max_run_time" in settings["selection_criteria"]):
        output *= (time.time() - process.create_time() < settings["selection_criteria"]["max_run_time"])

    return output

def generate_dict_with_info_detailed(process,settings):
    output_dict = dict()

    try:

        if("exe" in settings["detailed_output"] and process):
            output_dict["exe"] = process.name()

        if("user" in settings["detailed_output"]):
            output_dict["user"] = process.username()

        if("script" in settings["detailed_output"]):
            if(len(process.cmdline())>0):
                output_dict["script"] = process.cmdline()[-1]
            else:
                output_dict["script"] = np.nan()

        if("cpu_time" in settings["detailed_output"]):
            output_dict["cpu_time"] = sum(process.cpu_times()[:2])

        if("create_time" in settings["detailed_output"]):
            output_dict["create_time"] = process.create_time()

        if("time_since_creation" in settings["detailed_output"]):
            output_dict["time_since_creation"] = time.time() - process.create_time()

        if("time_active_ratio" in settings["detailed_output"]):
            output_dict["time_active_ratio"] = sum(process.cpu_times()[:2])/(time.time() - process.create_time())

        if("pid" in settings["detailed_output"]):
            output_dict["pid"] = process.pid

        if("status" in settings["detailed_output"]):
            output_dict["status"] = process.status()

        if("memory_percent" in settings["detailed_output"]):
            output_dict["memory_percent"] = process.memory_percent()

        if("cpu_percent" in settings["detailed_output"]):
            output_dict["cpu_percent"] = process.cpu_percent()

        if("memory_total" in settings["detailed_output"]):
            output_dict["memory_total"] = process.memory_info().rss

        return output_dict
    
    except psutil.NoSuchProcess:  # Catch the error caused by the process no longer existing
        return dict()


def get_info_of_running_processes(settings):  
    output = list()
    running_processes = psutil.process_iter()
    for process in running_processes:
        if(check_whether_process_is_of_interest(process,settings)):
            tmp = generate_dict_with_info_detailed(process,settings)
            if(len(tmp) > 0):
                output.append(tmp)
                set_of_pids.add(process.pid)
    return pd.DataFrame(output)

def write_out_running_job_information(input,folder_name,file_name):
    if(len(input)>0):
        input.to_json(folder_name + file_name)

