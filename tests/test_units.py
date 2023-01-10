import sys

sys.path.append("..")

import subprocess
import time

import pytest

from src.detailed_information import get_info_of_running_processes
from src.finished_information import check_for_finished_finished_jobs
from src.settings_manager import check_required_entries_in_settings, read_settings


def test_root_info_extraction():
    settings = read_settings("./settings.json")
    process = subprocess.Popen(["python", "process_example.py", "-t", "5"])
    time.sleep(3)
    df = get_info_of_running_processes(settings)
    assert len(df) > 0
    assert (df["script"] == "process_example.py").any
    process.wait()


def test_find_finished_job():
    settings = read_settings("./settings.json")
    process = subprocess.Popen(["python", "process_example.py", "-t", "5"])
    time.sleep(3)
    df_1 = get_info_of_running_processes(settings)
    time.sleep(5)
    df_2 = get_info_of_running_processes(settings)
    list = check_for_finished_finished_jobs(df_2)
    assert len(list) > 0
    process.wait()


def test_find_two_finished_jobs():
    settings = read_settings("./settings.json")
    process_1 = subprocess.Popen(["python", "process_example.py", "-t", "5"])
    process_2 = subprocess.Popen(["python", "process_example.py", "-t", "10"])
    time.sleep(3)
    df_1 = get_info_of_running_processes(settings)
    time.sleep(5)
    df_2 = get_info_of_running_processes(settings)
    list_1 = check_for_finished_finished_jobs(df_2)
    time.sleep(5)
    df_3 = get_info_of_running_processes(settings)
    list_2 = check_for_finished_finished_jobs(df_3)
    assert len(list_2) > 0
    process_1.wait()
    process_2.wait()


def test_read_test_settings():
    settings = read_settings("./settings.json")
    assert settings == (
        settings
        | {
            "selection_criteria": {
                "exe": "python",
                "status": ["running", "sleeping", "disk-sleep"],
                "user": "ga63zay",
                "max_run_time": 604800,
            }
        }
    )


def test_required_exeptions():
    example_settings = {"selection_criteria": {}, "output": []}
    with pytest.raises(Exception):
        check_required_entries_in_settings(example_settings)


def test_work_flow_required_exeptions():
    example_settings = {"selection_criteria": {}, "output": [], "work_flow": {}}
    with pytest.raises(Exception):
        check_required_entries_in_settings(example_settings)


def test_conditional_required_exeptions():
    example_settings = {
        "selection_criteria": {},
        "output": [],
        "work_flow": {
            "loop_interval": 60,
            "with_detailed_output": True,
            "with_finished_jobs_output": True,
            "with_summary": True,
        },
    }
    with pytest.raises(Exception):
        check_required_entries_in_settings(example_settings)
