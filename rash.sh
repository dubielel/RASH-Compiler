#!/bin/bash

usage() { echo "$0 usage:" && grep " .)\ #" $0; exit 0; }

translate() {
    echo $1;
    echo $(basename $1)".c"
    new_name=$(basename $1)".c"
    python main.py $1 ".rashc/"
}

run_c() {
    cd .rashc/
    mkdir -p build-dir
    cd build-dir
    cmake ..
    make
    [ $? -eq 0 ] && ./rashProject
}

[ $# -eq 0 ] && usage

while getopts ":r:hf:" arg; do
    case "$arg" in
        f) # Compile code from the file
            translate "${OPTARG}"
            ;;
        r) # Compile with CMake
			echo "${OPTARG}"
            translate "${OPTARG}"
            [ $? -eq 0 ] && run_c "${OPTARG}"
            ;;
        h | *) # Display this message
            usage
            exit 0
            ;;
    esac
done

