#!/usr/bin/env bash

command=$(which python3)
main_path="../artificial_idiot/main.py"
outputf="../outputs/step.txt"

timeit=$1

if [[ $timeit = true ]] ; then
    command="time $command"
fi

out=""
> $outputf

for number in {1..20} ; do
    val=$($command $main_path ../tests/part_a/sample$number.json brief)
    echo -e "$val" >> $outputf
    out="$out$val\n"
done

echo -e $out