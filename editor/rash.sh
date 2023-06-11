#!/bin/bash

usage() { echo "$0 usage:" && grep " .)\ #" $0; exit 0; }

run() {
    echo $1;
    new_name=$(basename $1)".c"
    python main.py $1 ".rashc/${new_name}"
    echo $(basename $1)".c"
}

[ $# -eq 0 ] && usage

while getopts ":hf:" arg; do
    case "$arg" in
        f) # Run code from the file
            run "${OPTARG}"
            ;;
        h | *) # Display this message
            usage
            exit 0
            ;;
    esac
done


