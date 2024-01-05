#!/bin/bash

# create my timestamp for naming the log file
timestamp=$(date +"%Y-%m-%d_%T")

# set the log output directory
logDir=/Users/scott/Logs/custom_startup_script/v4/

# format the timestamp by replacing ":" from the filename (otherwise macOS will moan like a bitch)
ts=${timestamp//[:]/-}

# set value for output log
logFile=$logDir$ts.txt

printf "%s\tCommence logging of custom startup script\n" "$(/usr/local/bin/gdate +"%T.%4N")" > $logFile


# Since there is an issue with Transmission starting up before the required
# disks have been mounted, this script will run at startup, check if
# Transmission is running, terminate the process if it is, and loop over the
# mounted volumes until /Volumes/iMacHD is mounted. Once iMacHD is mounted, launch Transmission


# Transmission
#####################################################################################################################
# Reference site:
# https://stackoverflow.com/questions/1821886/check-if-mac-process-is-running-using-bash-by-process-name
printf "%s\tCheck for existing Transmission service\n" "$(/usr/local/bin/gdate +"%T.%4N")" >> $logFile

PROCESS=Transmission
number=$(ps aux | grep -v grep | grep -ci Transmission)

if [ $number -gt 0 ]
    then
        printf "%s\tTransmission is running. Kill it!\n" "$(/usr/local/bin/gdate +"%T.%4N")" >> $logFile
        /usr/bin/killall $PROCESS
        printf "%s\tTransmission killed\n" "$(/usr/local/bin/gdate +"%T.%4N")" >> $logFile
        sleep 2
else
    printf "%s\tTransmission process not found\n" "$(/usr/local/bin/gdate +"%T.%4N")" >> $logFile
fi


# while loop to check mounted volumes
while ! [[ $(mount | awk '$3 == "/Volumes/iMacHD" {print $3}') != "" ]];
do
    printf "%s\tiMacHD disk not mounted yet. Wait for 2 seconds\n" "$(/usr/local/bin/gdate +"%T.%4N")" >> $logFile
    sleep 2
done
printf "%s\tiMacHD disk successfully mounted. Continue\n" "$(/usr/local/bin/gdate +"%T.%4N")" >> $logFile


# now we can launch Transmission, Radarr and Sonarr
printf "%s\tStarting Transmission\n" "$(/usr/local/bin/gdate +"%T.%4N")" >> $logFile
/usr/bin/open -a Transmission
status=$?
printf "%s\tRequest to start Transmission returned: %s\n" "$(/usr/local/bin/gdate +"%T.%4N")" $status >> $logFile
#####################################################################################################################


# Sonarr
#####################################################################################################################
printf "%s\tWaiting 1 second before starting Sonarr service\n" "$(/usr/local/bin/gdate +"%T.%4N")" >> $logFile
sleep 1s

printf "%s\tStarting Sonarr\n" "$(/usr/local/bin/gdate +"%T.%4N")" >> $logFile
/usr/bin/open -a Sonarr
status=$?
printf "%s\tRequest to start Sonarr returned: %s\n" "$(/usr/local/bin/gdate +"%T.%4N")" $status >> $logFile
# Sonarr
#####################################################################################################################


# Radarr
#####################################################################################################################
printf "%s\tWaiting 1 second before starting Radarr service\n" "$(/usr/local/bin/gdate +"%T.%4N")" >> $logFile
sleep 1s

printf "%s\tStarting Radarr\n" "$(/usr/local/bin/gdate +"%T.%4N")" >> $logFile
/usr/bin/open -a Radarr
status=$?
printf "%s\tRequest to start Radarr returned: %s\n" "$(/usr/local/bin/gdate +"%T.%4N")" $status >> $logFile
# Radarr
#####################################################################################################################


# Sony speaker
#####################################################################################################################
# Finally, connect the Sony bluetooth speaker if headphones not plugged in
printf "%s\tFinally, let\'s connect the Sony Bluetooth speaker\n" "$(/usr/local/bin/gdate +"%T.%4N")" >> $logFile
audio_output=$(system_profiler SPAudioDataType | grep "Output Source:" | awk '{print $3}')
if [  $audio_output != "Headphones" ]
    then
        /usr/local/bin/blueutil --connect "SRS-BT100"
        status=$?
        printf "%s\tBluetooth connection attempt returned: %s\n" "$(/usr/local/bin/gdate +"%T.%4N")" $status >> $logFile
else
    printf "%s\tHeadphones are plugged in, so not connecting to bluetooth.\n" "$(/usr/local/bin/gdate +"%T.%4N")" >> $logFile

fi
#####################################################################################################################


printf "%s\tStartup complete. Exiting!\n" "$(/usr/local/bin/gdate +"%T.%4N")" >> $logFile
exit 0
