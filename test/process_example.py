import argparse
import time

argParser = argparse.ArgumentParser()
argParser.add_argument(
    "-t",
    "--time_to_sleep",
    help="time to sleep in seconds",
    default="5",
    nargs="?",
    type=int,
)
args = argParser.parse_args()

time.sleep(args.time_to_sleep)
