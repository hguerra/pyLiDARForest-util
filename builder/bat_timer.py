import argparse
import os
from datetime import datetime
from subprocess import Popen
from time import sleep

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Alarm Clock")
    parser.add_argument("-t", "--time", type=str, required=True, help="Time in 24h. Example: '18:30'")
    parser.add_argument("-s", "--script", type=str, required=True, help="Script to execute. Example: 'zonal_stats.bat'")
    args = parser.parse_args()

    if not os.path.isfile(args.script):
        raise RuntimeError("Script must be a file")

    print("Wake me up at: '{}' with the script '{}'".format(args.time, args.script))

    current_time = datetime.now()
    final_time = datetime.strptime(args.time, "%H:%M")
    final_time = current_time.replace(hour=final_time.time().hour, minute=final_time.time().minute,
                                      second=final_time.time().second, microsecond=0)

    time_delta = final_time - current_time
    seconds = time_delta.total_seconds()
    if seconds > 0:
        sleep(seconds)

    print("Running script '{}'...".format(args.script))
    Popen(args.script)
