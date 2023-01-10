"""
A simple process data aggregator tool to monitor processes on your computer.

Copyright (c) 2022, Moritz Neuberger
All rights reserved.

License:  Standard 3-clause BSD
"""


import argparse
import os

import daemon
import lockfile

from src.process_information_aggregator import main

argParser = argparse.ArgumentParser()
argParser.add_argument(
    "-s", "--settings", help="path to settings file", default="settings.json", nargs="?"
)
args = argParser.parse_args()


f_stdout = open("stdout.log", "w+")
f_stderr = open("stderr.log", "w+")

context = daemon.DaemonContext(
    working_directory=f"{os.getcwd()}",
    umask=0o002,
    pidfile=lockfile.FileLock(f"{os.getcwd()}" + "/daemon_process_root_scripts.pid"),
    stdout=f_stdout,
    stderr=f_stderr,
)

with context:
    main(args.settings)
