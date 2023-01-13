import json
import os

hard_coded_settings = {
    "date_format": "%Y_%m_%d",
    "date_and_time_format": "%Y_%m_%d_%H_%M_%S",
}


def check_required_entries_in_settings(input):

    requirements_base = ["selection_criteria", "detailed_output", "work_flow"]
    for req in requirements_base:
        if not req in input:
            raise Exception(f"Required parameter {req} not set. Exit.")

    conditional_requirements = {
        "with_finished_jobs_output": "finished_output",
        "with_summary": "summary_output",
    }
    for creq_k, creq_v in conditional_requirements.items():
        if (
            creq_k in input["work_flow"]
            and input["work_flow"][creq_k]
            and not creq_v in input
        ):
            raise Exception(
                "Conditionally required parameter {} not set. It is required when {} is given. Exit.".format(
                    creq_v, creq_k
                )
            )

    requirements_work_flow = ["loop_interval"]
    for req in requirements_work_flow:
        if not req in input["work_flow"]:
            raise Exception(f"Required parameter {req} not set. Exit.")

    conditional_work_flow_requirements = {
        "with_detailed_output": "folder_detailed_output",
        "with_finished_jobs_output": "folder_finished_jobs",
        "with_finished_jobs_output": "summary_update_every_n_loops",
        "with_summary": "folder_summary",
        "with_summary": "summary_update_every_n_loops",
        "with_graphical_output": "folder_graphs",
    }
    for creq_k, creq_v in conditional_work_flow_requirements.items():
        if (
            creq_k in input["work_flow"]
            and input["work_flow"][creq_k]
            and not creq_v in input["work_flow"]
        ):
            raise Exception(
                "Conditionally required parameter {} not set. It is required when {} is given. Exit.".format(
                    creq_v, creq_k
                )
            )

    if not "cwd" in input["work_flow"]:
        input["cwd"] = os.getcwd()


def read_settings(file_name):
    settings = dict()
    with open(file_name) as json_file:
        settings = json.load(json_file).copy()
    check_required_entries_in_settings(settings)
    return settings
