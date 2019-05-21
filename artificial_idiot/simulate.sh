#!/bin/bash
FILE_PATH="./log/"
FILE_EXTENSION=".log"
for run in {1..10}
do
  echo $run
  result="python -m referee artificial_idiot:red artificial_idiot:green artificial_idiot:blue -v 0"
  echo $(python -m referee artificial_idiot:red artificial_idiot:green artificial_idiot:blue -v 0) 
done
