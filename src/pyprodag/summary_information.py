from datetime import datetime

import pandas as pd

from .file_system_interaction import *


def extract_info_of_individual_file_from_summary(file, settings):
    try:
        df = pd.read_json(file)
        output = dict()
        output["timestamp"] = extract_timestamp_from_file_name(file)
        output["time"] = datetime.fromtimestamp(output["timestamp"])
        if "cpu_over_time" in settings["summary_output"]:
            output["cpu_over_time"] = df["cpu_percent"].sum() / 100.0
        if "n_jobs_over_time" in settings["summary_output"]:
            output["n_jobs_over_time"] = len(df)
        if "memory_over_time" in settings["summary_output"]:
            output["memory_over_time"] = (
                df["memory_total"].sum() / 1024.0 / 1024.0 / 1024.0
            )
        if "ratio_status_running_over_time" in settings["summary_output"]:
            output["ratio_status_running_over_time"] = len(
                df[df["status"] == "running"]
            ) / (
                len(df[df["status"] == "running"])
                + len(df[df["status"] == "sleeping"])
                + len(df[df["status"] == "disk-sleep"])
            )
        return output
    except ValueError:
        print(f"Error while opening file {file}. Will skip it.")
        return dict()


def generate_summary(folder_name, settings):
    list_of_files = generate_file_list_of_today(folder_name)
    output = list()
    for file in list_of_files:
        output.append(extract_info_of_individual_file_from_summary(file, settings))
    return pd.DataFrame(output)


def write_summary_to_file(summary, folder_name, file_name):
    summary.to_json(folder_name + file_name)
