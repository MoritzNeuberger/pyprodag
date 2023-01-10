import json
from os import path

import pandas as pd

from .detailed_information import *


def generate_dict_with_info_finished(pid, previous_data, settings):
    output_dict = dict()

    if "pid" in settings["finished_output"]:
        output_dict["pid"] = pid

    row = previous_data.loc[previous_data["pid"] == pid]

    if "exe" in settings["finished_output"]:
        output_dict["exe"] = row["exe"].item()

    if "user" in settings["finished_output"]:
        output_dict["user"] = row["user"].item()

    if "script" in settings["finished_output"]:
        output_dict["script"] = row["script"].item()

    if "time_since_creation" in settings["finished_output"]:
        output_dict["time_since_creation"] = row["time_since_creation"].item()

    if "memory_total" in settings["finished_output"]:
        output_dict["memory_total"] = row["memory_total"].item()

    if "time_active_ratio" in settings["finished_output"]:
        output_dict["time_active_ratio"] = row["time_active_ratio"].item()

    if "cpu_time" in settings["finished_output"]:
        output_dict["cpu_time"] = row["cpu_time"].item()

    return output_dict


def check_for_finished_finished_jobs(data):
    output = set()

    if len(data) > 0:
        tmp = set_of_pids.copy()
        for pid in tmp:
            if bool((data["pid"] != pid).all()):
                set_of_pids.remove(pid)
                output.add(pid)
        return output

    else:
        tmp = set_of_pids.copy()
        set_of_pids.clear()
        return tmp


def get_info_of_individual_finished_processes(
    finished_jobs_pid, previous_data, folder_name, file_name, settings
):
    if len(previous_data) > 0 and len(finished_jobs_pid) > 0:
        output = list()
        for pid in finished_jobs_pid:
            output.append(
                generate_dict_with_info_finished(pid, previous_data, settings)
            )
        finished_data = pd.DataFrame(output)

        if path.isfile(folder_name + file_name):
            with open(folder_name + file_name) as json_file:
                file = json.load(json_file)
                input_df = pd.DataFrame(file["individual_finished_data"]).copy()
        else:
            input_df = pd.DataFrame()

        return pd.concat([input_df, finished_data], ignore_index=True)
    else:
        if path.isfile(folder_name + file_name):
            with open(folder_name + file_name) as json_file:
                file = json.load(json_file)
                input_df = pd.DataFrame(file["individual_finished_data"]).copy()
        else:
            input_df = pd.DataFrame()
        return input_df


def generate_finished_data_summary(finished_data_individual):
    if len(finished_data_individual) > 0:
        output = dict()
        output["n_by_user"] = dict()
        output["cpu_time_by_user"] = dict()
        list_of_users = list(dict.fromkeys(finished_data_individual["user"].tolist()))
        print("list_of_users: ", list_of_users)
        for user in list_of_users:
            output["n_by_user"][user] = 0
            output["cpu_time_by_user"][user] = 0
        for index, row in finished_data_individual.iterrows():
            output["n_by_user"][row["user"]] += 1
            output["cpu_time_by_user"][row["user"]] += row["cpu_time"]
        return pd.DataFrame(output)
    else:
        return pd.DataFrame()


def write_out_finished_job_information(
    finished_data_individual: pd.DataFrame,
    finished_data_summary: pd.DataFrame,
    folder_name,
    file_name,
):
    print(
        "len(finished_data_individual):",
        len(finished_data_individual),
        " - len(finished_data_summary):",
        len(finished_data_summary),
    )
    if len(finished_data_individual) > 0 and len(finished_data_summary) > 0:
        json_file = {
            "individual_finished_data": finished_data_individual.to_dict(),
            "summary_finished_data": finished_data_summary.to_dict(),
        }
        with open(folder_name + file_name, "w") as outfile:
            json.dump(json_file, outfile)
