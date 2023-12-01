package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

// Part I
func extractCalibrationValue(line string) int {
	re := regexp.MustCompile("[0-9]")
	allNumbers := re.FindAllString(line, -1)
	calibrationValueString := allNumbers[0] + allNumbers[len(allNumbers)-1]
	calibrationValueInt, _ := strconv.Atoi(calibrationValueString)
	return calibrationValueInt
}

// preserve leading and trailing character to deal with overlaps.
var Numbers = map[string]string{
	"one":   "o1e",
	"two":   "t2o",
	"three": "t3e",
	"four":  "f4r",
	"five":  "f5e",
	"six":   "s6x",
	"seven": "s7n",
	"eight": "e8t",
	"nine":  "n9e",
}

// Part II
func extractCalibrationValueSmarter(line string) int {
	for k, v := range Numbers {
		line = strings.ReplaceAll(line, k, v)
	}
	return extractCalibrationValue(line)
}

func main() {
	file, _ := os.Open("aoc_1.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	partOneTotal, partTwoTotal := 0, 0
	for scanner.Scan() {
		line := scanner.Text()
		partOneTotal += extractCalibrationValue(line)
		partTwoTotal += extractCalibrationValueSmarter(line)
	}
	fmt.Printf("Part 1: %v\n", partOneTotal)
	fmt.Printf("Part 2: %v\n", partTwoTotal)
}
