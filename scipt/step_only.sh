#!/usr/bin/env bash

command=$(which python3)
main_path="../artificial_idiot/main.py"

args=$1
timeit=$2

if [ $timeit = true ] ; then
    command="time $command"
fi

out=""

for number in {1..18} ; do
    out=$out$($command $main_path ../tests/part_a/sample$number.json $args)
done

out > ../outputs/