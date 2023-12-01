#!/bin/bash

DAY=$1
URL="https://adventofcode.com/2023/day/${DAY}/input"
SESSIONID=$2
curl -s $URL -o "aoc_${DAY}.txt" -H "cookie: session=${SESSIONID}" 