package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

// Returns the maximum number of given color in the sample.
func max(line string, color string) int {
	pattern := regexp.MustCompile(fmt.Sprintf(`(\d+)\s+%s`, color))
	matches := pattern.FindAllStringSubmatch(line, -1)

	var highestNumber int
	for _, match := range matches {
		currentNumber, _ := strconv.Atoi(match[1])
		if currentNumber > highestNumber {
			highestNumber = currentNumber
		}
	}
	return highestNumber
}

func main() {
	file, _ := os.Open("aoc_2.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	games := make(map[int][]int)
	index := 1
	for scanner.Scan() {
		line := scanner.Text()
		games[index] = []int{max(line, "red"), max(line, "green"), max(line, "blue")}
		index++
	}
	partOneTotal, partTwoTotal := 0, 0
	for i, v := range games {
		if v[0] <= 12 && v[1] <= 13 && v[2] <= 14 {
			partOneTotal += i
		}
		partTwoTotal += v[0] * v[1] * v[2]
	}
	fmt.Printf("Part 1: %v\n", partOneTotal)
	fmt.Printf("Part 2: %v\n", partTwoTotal)
}
