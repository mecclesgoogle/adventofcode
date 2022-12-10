#!/bin/bash

DAY=$1
URL="https://adventofcode.com/2022/day/${DAY}/input"
SESSIONID=$2
curl -s $URL -o "elves_${DAY}.txt" -H "cookie: session=${SESSIONID}" 