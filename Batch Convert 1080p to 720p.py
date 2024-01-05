#!/usr/bin/env python

import random, string, datetime, time, os, sys

# create my timestamp for naming the log file
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

####################################################################################
# Global variables

# set the log output directory
logDir = '/Users/scott/Logs/ffmpeg/'

# Define log file name with current date/timestamp
my_logFile = logDir + timestamp + ".txt"

ff_bin = '/usr/local/bin/ffmpeg -i'
ff_switches = '-s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 -loglevel 16'  # Loglevel 16 = errors only


# End Globals

####################################################################################
def logger(logdata):
    # The following function accepts a single input string which is appended to a timestamp
    # The result is written to the log file
    #
    # Examples:
    # logdata = 'FAILURE || Failure message here'
    # logdata = "  INFO  || Converting \"{}\"".format(inFile)
    # logdata = "SUCCESS || We did something properly here!"

    # Open logfile
    logfile_pipe = open(my_logFile, "a+")

    logTS = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")[:-2]
    logdata_string = logTS + ' || ' + logdata + "\r\n"
    logfile_pipe.write(logdata_string)

    # Close logfile
    logfile_pipe.close()


####################################################################################
logger("  INFO  || Starting downgrade script. Checking for input file")

if len(sys.argv) == 1:
    logger("FAILURE || No file found to convert. Exiting.....")
    quit()

if len(sys.argv[1:]) > 2:
    logger("  INFO  || Converting \"{}\" files".format(len(sys.argv[1:])))

for f in sys.argv[1:]:
    inFile = f
    tmpFile = ""
    inFile_path, inFile_name = os.path.split(inFile)
    if inFile[:-4].endswith('1080p'):
        tmpFile = inFile[:-9] + "_720p" + inFile[-4:]
    else:
        tmpFile = inFile[:-4] + "_720p" + inFile[-4:]
    tmpFile = inFile[:-4] + "_720p" + inFile[-4:]
    if tmpFile.endswith('1080p'):
        tmpFile = tmpFile[0:-5]
    trashDir = '/Users/scott/.Trash/'

    # print(r"""
    #    Converting: "{}"
    #     File name: "{}"
    #     File path: "{}"
    # """.format(inFile, inFile_name, inFile_path))

    logger("  INFO  || Downgrading \"{}\" from 1080p to 720p".format(inFile))
    logger("  INFO  || Outputting new file to: \"{}\" from 1080p to 720p".format(tmpFile))

    # Convert File
    conversion_result = os.system("{} \"{}\" {} \"{}\"".format(ff_bin, inFile, ff_switches, tmpFile))

    if conversion_result == 0:
        logger("SUCCESS || Successfully downgraded \"{}\" to 720p!".format(inFile))
        logger("  INFO  || Deleting temporary file: \"{}\"".format(tmpFile))
        delTmpFile = os.system("mv \"{}\" \"{}\"".format(tmpFile, inFile))
        if delTmpFile == 0:
            logger("SUCCESS || Successfully deleted temp file: \"{}\"!".format(tmpFile))
        else:
            logger("FAILURE || Failed to delete temp file \"{}\". Please delete manually".format(tmpFile))
    else:
        logger("FAILURE || Failed to downgrade input file \"{}\". Return code: \"{}\". Deleting temp file!!".format(
            tmpFile, conversion_result))
        os.system("mv \"{}\" \"{}\"".format(tmpFile, trashDir))

logger("  INFO  || Exiting......")