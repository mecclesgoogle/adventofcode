package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	file, _ := os.Open("aoc_9.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	sequences := make([][]string, 0)
	for scanner.Scan() {
		line := scanner.Text()
		sequences = append(sequences, strings.Fields(line))
	}
	intSequences := make([][]int64, len(sequences))
	for i, v := range sequences {
		for _, v2 := range v {
			intVal, _ := strconv.Atoi(v2)
			intSequences[i] = append(intSequences[i], int64(intVal))

		}
	}
	var partOne int64
	for _, v := range intSequences {
		partOne += CalculateSequence(v)

	}
	fmt.Println("Part 1:", partOne)
	var partTwo int64
	for _, v := range intSequences {
		partTwo += CalculateSequencePartTwo(v)
	}
	fmt.Println("Part 2:", partTwo)
}

func sum(list []int64) int64 {
	var total int64
	for _, v := range list {
		total += v
	}
	return total
}

func CalculateSequence(sequence []int64) int64 {
	diffs := AllDiffs(sequence)
	var addend int64
	for i := len(diffs) - 1; i > 1; i-- {
		addend = addend + diffs[i-1][len(diffs[i-1])-1]
	}
	return addend + sequence[len(sequence)-1]
}

func CalculateSequencePartTwo(sequence []int64) int64 {
	diffs := AllDiffs(sequence)
	var addend int64
	for i := len(diffs) - 1; i > 1; i-- {
		addend = diffs[i-1][0] - addend
	}
	return sequence[0] - addend
}

func AllDiffs(sequence []int64) [][]int64 {
	diffs := [][]int64{sequence}
	latestDiff := sequence
	for sum(latestDiff) != 0 {
		latestDiff = Diffs(latestDiff)
		diffs = append(diffs, latestDiff)
	}
	return diffs
}

func Diffs(sequence []int64) []int64 {
	d := make([]int64, 0)
	for i := 0; i < len(sequence)-1; i++ {
		d = append(d, sequence[i+1]-sequence[i])
	}

	return d
}
