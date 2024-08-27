#!/usr/local/bin/python3.11
import subprocess
import pandas as pd
import datetime as dt
import humanize
import os

#############################################################################################################
# Global variables

START_TIME = dt.datetime.now()
START_TIME_FLOOR = START_TIME.replace(second=0, microsecond=0)
LOG_TIME = START_TIME_FLOOR.isoformat()
MARKER_CHAR = '#'
DATA_FILE = '/Users/scott/Local/Data/System/disk_stats/usage_stats.csv'
# End Globals
#############################################################################################################


#############################################################################################################
def get_diskutil_info(filesystem):
    diskutil_cmd = f'/usr/sbin/diskutil info {filesystem}'
    grep_cmd = 'grep -e "Volume Name:" -e "Container Total Space:" -e "Container Free Space:"'
    get_info_cmd = f'{diskutil_cmd} | {grep_cmd}'

    # Execute the 'diskutil' command and capture the output
    try:
        diskutil_output = subprocess.run(
            get_info_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).stdout.decode('utf-8')
        return diskutil_output
    # Handle return of any non-zero statuses
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:  # No matches found
            print('Nothing found.. Exiting')
            exit(0)
        else:  # Other errors (e.g., file not found, permission denied, etc.)
            print(f"We encountered an error:\t {str(e.stderr.decode('utf-8'))}")
            exit(1)
#############################################################################################################


#############################################################################################################
def get_mounted_volumes():
    # System commands
    df_cmd = 'df -h'
    grep_cmd = 'grep -v -e "disk1s1s1" -e "devfs" -e "disk1s2" -e "disk1s4" -e "disk1s6" -e "auto_home" -e "TimeMachin"'
    awk_cmd = "awk '{print $1}'"
    get_vols_cmd = f'{df_cmd} | {grep_cmd} -e "Mounted" | {awk_cmd}'

    # Execute the 'df' command and capture the output
    try:
        df_output = subprocess.run(
            get_vols_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).stdout.decode('utf-8').split('\n')

        # Drop any empty list values
        volume_list = [x for x in df_output if len(x) > 0]
        return volume_list

    # Handle return of any non-zero statuses
    except subprocess.CalledProcessError as e:
        if e.returncode == 1: # No matches found
            print('Nothing found.. Exiting')
            exit(0)
        else: # Other errors (e.g., file not found, permission denied, etc.)
            print(f"We encountered an error:\t {str(e.stderr.decode('utf-8'))}")
            exit(1)
#############################################################################################################


#############################################################################################################
def percentage(part, whole):
  return round((100 * float(part) / float(whole)), 2)
#############################################################################################################


#############################################################################################################
# Function to convert bytes to gigabytes
def to_gb(bytes_val):
    return round((bytes_val / 1024 ** 3), 3)
#############################################################################################################


#############################################################################################################
# Function to convert bytes to terabytes
def to_tb(bytes_val):
    return round((bytes_val / 1024 ** 4), 3)
#############################################################################################################


#############################################################################################################
def write_df_to_csv(df):
    # Check if the file already exists
    if not os.path.isfile(DATA_FILE):
        logging_dt = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
        print(f'{logging_dt}  Creating new file, as no file exists at:\t "{DATA_FILE}"')
        df.to_csv(DATA_FILE, mode='w', index=False, header=True)
    else:  # If it exists, append without writing the header
        df.to_csv(DATA_FILE, mode='a', index=False, header=False)
#############################################################################################################


#############################################################################################################
def main():
    print(f'\n\n{MARKER_CHAR * 120}')
    logging_dt = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
    print(f'{logging_dt}  Collect and log usage stats on all mounted disks')
    print(f'{logging_dt}  Logged execution time:\t {START_TIME_FLOOR}')

    disks_list = get_mounted_volumes()
    logging_dt = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
    print(f'{logging_dt}  Total mounted disks discovered:\t {len(disks_list)}')

    # Initialize filtered_data list
    filtered_data = []

    for d in disks_list:
        # Tried both psutil and shutil, but neither returned correct data for my 18TB disks
        disk_info = get_diskutil_info(d)
        disk_info_list = str(disk_info).strip().split('\n')

        # Extract relevant information from the list
        volume_name = disk_info_list[0].split(":")[1].strip()
        if volume_name == 'macOS - Data':
            volume_name = 'macOS'

        # Extracting the total and free space in bytes
        total_space = int(disk_info_list[1].split("(")[1].split(")")[0].split(" ")[0].strip())
        free_space = int(disk_info_list[2].split("(")[1].split(")")[0].split(" ")[0].strip())

        # Calculate used space
        used_space = total_space - free_space

        # Append the parsed data to filtered_data list
        filtered_data.append({
            'Timestamp': LOG_TIME,
            'Disk': volume_name,
            'Capacity': total_space,
            'Capacity (TB)': to_tb(total_space),
            'Used Space': used_space,
            'Used Space (TB)': to_tb(used_space),
            '% Free': percentage(free_space, total_space),
            '% Used': percentage(used_space, total_space)
        })

    # Convert the filtered data into a DataFrame
    df = pd.DataFrame(filtered_data)
    df = df.sort_values(by='Disk', ascending=True).reset_index(drop=True)

    logging_dt = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
    print(f'{logging_dt}  Data collection completed.')
    print(f'{logging_dt}  Writing data to: "{DATA_FILE}"')
    write_df_to_csv(df)

    logging_dt = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
    print(f'{logging_dt}  Execution complete. Total runtime:\t {humanize.precisedelta(dt.datetime.now() - START_TIME)}')
    print(f'{MARKER_CHAR * 120}\n\n')


#############################################################################################################


#############################################################################################################
if __name__ == "__main__":
    main()
