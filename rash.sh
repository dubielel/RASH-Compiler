#!/bin/bash

usage() { echo "$0 usage:" && grep " .)\ #" $0; exit 0; }

run() {
    echo $1;
    new_name=$(basename $1)".c"
    python main.py $1 ".rashc/${new_name}"
    echo $(basename $1)".c"
}

run_c() {
	echo $1;
    cd .rashc/$(basename "$1")".c"
    mkdir -p build-dir
    cd build-dir
    cmake ..
    make
    ./rashProject;
}

[ $# -eq 0 ] && usage

while getopts ":r:hf:" arg; do
    case "$arg" in
        f) # Run code from the file
            run "${OPTARG}"
            ;;
        r) # Compile with CMake, use this after -f option
			echo "${OPTARG}"
            run_c "${OPTARG}"
            ;;
        h | *) # Display this message
            usage
            exit 0
            ;;
    esac
done

