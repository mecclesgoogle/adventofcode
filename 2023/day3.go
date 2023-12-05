package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"regexp"
	"strconv"
)

type Number struct {
	value int
	row   int
	start int
	end   int
}

func main() {
	file, _ := os.Open("aoc_3.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var partOneTotal int
	var partTwoTotal int

	var rowNumber int
	numberRe := regexp.MustCompile(`\d+`)
	symbolRe := regexp.MustCompile(`[^\d\.]`)
	gearRe := regexp.MustCompile(`\*`)

	gearLocs := make([][]int, 0)
	symbolLocs := make([][]int, 0)
	numberLocs := make([]Number, 0)

	for scanner.Scan() {
		line := scanner.Text()
		numberMatches := numberRe.FindAllStringIndex(line, -1)
		for _, n := range numberMatches {
			value, _ := strconv.Atoi(line[n[0]:n[1]])
			numberLocs = append(numberLocs, Number{value, rowNumber, n[0], n[1]})
		}

		symbolMatches := symbolRe.FindAllStringIndex(line, -1)
		for _, n := range symbolMatches {
			symbolLocs = append(symbolLocs, []int{rowNumber, n[0]})
		}
		gearMatches := gearRe.FindAllStringIndex(line, -1)
		for _, n := range gearMatches {
			gearLocs = append(gearLocs, []int{rowNumber, n[0]})
		}
		rowNumber++
	}

	for _, n := range numberLocs {
		if isNumberNextToSymbol(n, symbolLocs) {
			partOneTotal += n.value
		}
	}

	fmt.Printf("Part 1: %v\n", partOneTotal)

	for _, g := range gearLocs {
		overlappingNumbers := getOverlappingNumbers(numberLocs, g[0], g[1])
		if len(overlappingNumbers) > 1 {
			partTwoTotal += overlappingNumbers[0].value * overlappingNumbers[1].value
		}
	}
	fmt.Printf("Part 2: %v\n", partTwoTotal)
}

func isNumberNextToSymbol(n Number, symbolLocs [][]int) bool {
	for row := n.row - 1; row <= n.row+1; row++ {
		for column := n.start - 1; column <= n.end; column++ {
			for _, a := range symbolLocs {
				if row == a[0] && column == a[1] {
					return true
				}
			}
		}
	}
	return false
}

func getOverlappingNumbers(numbers []Number, row int, column int) []Number {
	result := make([]Number, 0)

	for _, n := range numbers {
		var found bool
		if n.row >= row-1 && n.row <= row+1 {
			for i := n.start; i < n.end; i++ {
				if math.Abs(float64(column-i)) <= 1 {
					if !found {
						result = append(result, n)
					}
					found = true
				}
			}
		}
	}
	return result
}
