#!/usr/bin/env bash

command=$(which python3)
main_path="../artificial_idiot/main.py"

for file in ../tests/part_a/*.json ; do
    filename=$(basename -- "$file")
    extension="${filename##*.}"
    filename="${filename%.*}"
    $command $main_path $file > ../outputs/$filename.txt
done