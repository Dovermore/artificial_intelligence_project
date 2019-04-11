#!/usr/bin/env bash

command=$(which python3)
main_path="../artificial_idiot/search.py"
outputf="../outputs/analysis.txt"

timeit=$1

if [[ $timeit = true ]] ; then
    command="time $command"
fi

out=""
> $outputf

for number in {1..21} ; do
    echo $command $main_path ../tests/part_a/sample$number.json analysis
    val=$($command $main_path ../tests/part_a/sample$number.json analysis)
    echo -e "$val" >> $outputf
done
