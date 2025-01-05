#!/bin/bash
FILE="dataflow_files_20240801_05.txt"
if [ -z "$PROCESS" ]; then
	echo "Process not set! Running a array of jobs"
	exit 1
fi
FILE_TO_PROCESS=$(sed -n "$((PROCESS+1))p" "$FILE")
echo "[$(date)] PROCESS = $PROCESS, FILE_TO_PROCESS=$FILE_TO_PROCESS"

python3 test2.py "$FILE_TO_PROCESS"
BASE=$(basename "$FILE_TO_PROCESS")
OUTPUT_FILE="${BASE/.hdf5/_7645-7675.npy}"
mv "$OUTPUT_FILE" "$CONDOR_DIR_OUTPUT/$OUTPUT_FILE"

echo "[$(date)] DONE"
