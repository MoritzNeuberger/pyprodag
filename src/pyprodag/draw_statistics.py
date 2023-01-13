import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")

from .tol_colors import tol_cset


def cm_to_inch(value):
    return value / 2.54


cset = tol_cset("high-contrast")


def draw_summary(summary, finished_info, settings, folder_name):

    if "cpu_over_time" in settings["graphical_output"]:
        draw_cpu_over_time(summary, folder_name)

    if "n_jobs_over_time" in settings["graphical_output"]:
        draw_n_jobs_over_time(summary, folder_name)

    if "memory_over_time" in settings["graphical_output"]:
        draw_memory_over_time(summary, folder_name)

    if "ratio_status_running_over_time" in settings["graphical_output"]:
        draw_ratio_status_running_over_time(summary, folder_name)

    if "total_duration_of_jobs" in settings["graphical_output"]:
        draw_total_duration_of_jobs(finished_info, folder_name)


def draw_n_jobs_over_time(summary, folder_name):
    if len(summary) > 0:
        axis = summary.plot(x="time", y="n_jobs_over_time", color=cset.blue)
        axis.grid(visible=True, axis="both", which="both")
        axis.set_ylim(0, summary["n_jobs_over_time"].max() + 2)
        axis.set_xlabel("time")
        axis.set_ylabel("Number of running jobs")
        axis.set_title("Number of running jobs")
        plt.savefig(folder_name["graphs"] + "graph_n_jobs_over_time.png")
        plt.close()


def draw_memory_over_time(summary, folder_name):
    if len(summary) > 0:
        axis = summary.plot(x="time", y="memory_over_time", color=cset.yellow)
        axis.grid(visible=True, axis="both", which="both")
        axis.set_ylim(0, summary["memory_over_time"].max() + 2)
        axis.set_xlabel("time")
        axis.set_ylabel("Total memory [Gb]")
        axis.set_title("Total memory")
        plt.savefig(folder_name["graphs"] + "graph_memory_over_time.png")
        plt.close()


def draw_ratio_status_running_over_time(summary, folder_name):
    if len(summary) > 0:
        axis = summary.plot(
            x="time", y="ratio_status_running_over_time", color=cset.black
        )
        axis.grid(visible=True, axis="both", which="both")
        axis.set_ylim(0, 1.05)
        axis.set_xlabel("time")
        axis.set_ylabel("Status of jobs")
        axis.set_title("Status of jobs")
        plt.savefig(folder_name["graphs"] + "graph_ratio_status_running_over_time.png")
        plt.close()


def draw_cpu_over_time(summary, folder_name):
    if len(summary) > 0:
        axis = summary.plot(x="time", y="cpu_over_time", color=cset.red)
        axis.grid(visible=True, axis="both", which="both")
        axis.set_ylim(0, summary["cpu_over_time"].max() + 2)
        axis.set_xlabel("time")
        axis.set_ylabel("CPU usage [#cores]")
        axis.set_title("CPU usage")
        plt.savefig(folder_name["graphs"] + "graph_cpu_over_time.png")
        plt.close()


def draw_total_duration_of_jobs(finished_info, folder_name):
    if len(finished_info) > 0:
        axis = finished_info.plot.hist(
            column=["time_since_creation"],
            bins=10
            ** np.linspace(
                np.log10(max(finished_info["time_since_creation"].min() - 5, 0.1)),
                np.log10(finished_info["time_since_creation"].max() + 10),
                50,
            ),
            color=cset.red,
        )
        axis.grid(visible=True, axis="both", which="both")
        axis.set_xlabel("duration [s]")
        axis.set_ylabel("")
        axis.set_title("Total duration of jobs")
        if (finished_info["time_since_creation"] > 0).any():
            axis.set_xscale("log")
        plt.savefig(folder_name["graphs"] + "graph_total_duration_of_jobs.png")
        plt.close()
