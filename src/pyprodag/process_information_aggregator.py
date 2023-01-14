import time

import pandas as pd

from . import *


def single_loop_run(previous_data, settings, counter):

    folder_name, file_name = generate_folder_and_file_name(settings)

    data = get_info_of_running_processes(settings)

    if (
        "with_detailed_output" in settings["work_flow"]
        and settings["work_flow"]["with_detailed_output"]
    ):
        write_out_running_job_information(
            data, folder_name["detailed"], file_name["detailed"]
        )

    if (
        "with_finished_jobs_output" in settings["work_flow"]
        and settings["work_flow"]["with_finished_jobs_output"]
    ):
        list_of_finished_jobs = check_for_finished_finished_jobs(data)
        finished_info_individual = get_info_of_individual_finished_processes(
            list_of_finished_jobs,
            previous_data,
            folder_name["finished"],
            file_name["finished"],
            settings,
        )
        if counter == int(settings["work_flow"]["summary_update_every_n_loops"]):
            finished_info_summary = generate_finished_data_summary(
                finished_info_individual
            )
            write_out_finished_job_information(
                finished_info_individual,
                finished_info_summary,
                folder_name["finished"],
                file_name["finished"],
            )

    if (
        "with_summary" in settings["work_flow"]
        and settings["work_flow"]["with_summary"]
        and counter == int(settings["work_flow"]["summary_update_every_n_loops"])
    ):
        summary = generate_summary(folder_name, settings)
        write_summary_to_file(summary, folder_name["summary"], file_name["summary"])

        if "with_graphical_output" in settings["work_flow"]:
            draw_summary(summary, finished_info_individual, settings, folder_name)

    if "clean_up_at_new_day" in settings["work_flow"]:
        clean_up_at_new_day(folder_name)

    if counter >= int(settings["work_flow"]["summary_update_every_n_loops"]):
        counter = 0
    else:
        counter += 1

    return data, counter


def main(settings_file):
    settings = read_settings(settings_file)
    previous_data = pd.DataFrame()
    counter = 0
    while True:
        previous_data, counter = single_loop_run(previous_data, settings, counter)
        time.sleep(settings["work_flow"]["loop_interval"])
