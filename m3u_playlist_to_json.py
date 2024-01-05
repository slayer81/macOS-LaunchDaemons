import os, json, time, subprocess, pathlib
from datetime import datetime
from m3u_parser import M3uParser
# If the output file is lowercase, edit line 559:
# /usr/local/lib/python3.11/site-packages/m3u_parser/m3u_parser.py

# If the output log is too verbose, edit line 205:
# /usr/local/lib/python3.11/site-packages/m3u_parser/helper.py

dataDir = '/Users/scott/Local/Data/IPTV'
start_time = datetime.now()

##################################################################
def convert_m3u_playlist_to_json(file, stage_num):
    file_stem = pathlib.PurePosixPath(file).stem
    # https://pypi.org/project/m3u-parser/

    # If output file exists, move to /_Archive/
    output_file = '{}/{}.json'.format(dataDir, file_stem)
    p = pathlib.Path(output_file)
    if p.exists():
        print("{}\tStage {}:\tExisting output file exists:\t{}".format(str(datetime.now()), stage_num, output_file))
        dt_stamp = datetime.utcnow().strftime("%Y-%m-%d_%H.%M.%S")
        archive_path = '{}/_Archives'.format(dataDir)
        archive_filename = '{}-{}.json'.format(file_stem, dt_stamp)
        archive_file = '{}/{}'.format(archive_path, archive_filename)
        print("{}\tStage {}:\tArchiving to:\t{}".format(str(datetime.now()), stage_num, archive_file))
        result = os.system("mv -f \"{}\" \"{}\"".format(output_file, archive_file))
        if result == 0:
            print("{}\tStage {}:\tFile archive successful".format(str(datetime.now()), stage_num))
        else:
            print("{}\tStage {}:\tFile archive FAILED: {}. Exiting!".format(str(datetime.now()), stage_num, result))
            exit()

    # Instantiate the parser
    parser = M3uParser(timeout=5)

    # Parse the m3u file
    parser.parse_m3u(file, check_live=False)

    # Convert playlist to json and save to file
    parser.to_file(output_file)
    print("{}\tStage {}:\tSuccessful conversion of m3u to json:\t{}".format(str(datetime.now()), stage_num, output_file))
##################################################################


##################################################################
def get_target_files():
    get_files = subprocess.run(
        [
            "find", "{}".format(dataDir),
            "-type", "f",
            "-name", "*.m3u",
            "-depth", "1",
            "-mtime", "-1d",
            "-print"
        ], stdout=subprocess.PIPE
    )
    target_files = get_files.stdout.decode('utf-8').splitlines()
    return target_files
##################################################################


##################################################################
def main():
    stageNum: int = 0
    print("{}\tStage {}:\tStarting execution of: {}".format(str(datetime.now()), stageNum, __file__))
    stageNum += 1

    ################################################
    # Stage: Get target files
    ################################################
    print("{}\tStage {}:\tFetching playlist files from:\t{}".format(str(datetime.now()), stageNum, dataDir))
    targetFiles = get_target_files()
    stageNum += 1

    ################################################
    # Stage: Parse m3u playlist and convert to json
    ################################################
    for f in targetFiles:
        print("{}\tStage {}:\tConverting playlist file:\t{}".format(str(datetime.now()), stageNum, f))
        convert_m3u_playlist_to_json(f, stageNum)
    print("{}\tStage {}:\tConversion completed. Exiting.....".format(str(datetime.now()), stageNum))

##################################################################

if __name__ == "__main__":
    main()

print("Total execution time: {}".format(datetime.now() - start_time))










