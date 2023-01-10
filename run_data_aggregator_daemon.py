"""
A simple process data aggregator to monitor processes on a computer.

Copyright (c) 2022, Moritz Neuberger
All rights reserved.

License:  Standard 3-clause BSD
"""


from src.process_information_aggregator import main
import daemon
import os
import lockfile
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("-s", "--settings", help="path to settings file", default="settings.json", nargs='?')
args = argParser.parse_args()


f_stdout = open('stdout.log', 'w+')
f_stderr = open('stderr.log', 'w+')

context = daemon.DaemonContext(
    working_directory="{}".format(os.getcwd()),
    umask=0o002,
    pidfile=lockfile.FileLock("{}".format(os.getcwd()) + '/daemon_process_root_scripts.pid'),
    stdout=f_stdout,
    stderr=f_stderr
    )

with context:
    main(args.settings)
