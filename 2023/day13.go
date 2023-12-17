package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
)

func main() {
	file, _ := os.Open("aoc_13.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	shapes := make([][]string, 0)
	shapes = append(shapes, []string{})
	var index int
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			index++
			shapes = append(shapes, []string{})
			continue
		}
		shapes[index] = append(shapes[index], line)
	}

	var partOne int
	var partTwo int
	for _, v := range shapes {
		hr := reflectionScorePartOne(v)
		d := transposeStringArray(v)
		vr := reflectionScorePartOne(d)
		partOne += hr * 100
		partOne += vr

		hr2 := reflectionScorePartTwo(v)
		vr2 := reflectionScorePartTwo(d)
		partTwo += hr2 * 100
		partTwo += vr2
	}
	fmt.Println(partOne)
	fmt.Println(partTwo)

}

func transposeStringArray(s []string) []string {
	numRows, numCols := len(s), len(s[0])
	transposed := make([]string, 0)
	for i := 0; i < numCols; i++ {
		var tr string
		for j := 0; j < numRows; j++ {
			tr += string(s[j][i])
		}
		transposed = append(transposed, tr)
	}
	return transposed
}

func reflectionScorePartOne(a []string) int {
	for r := 1; r < len(a); r++ {
		above := slices.Clone(a[:r])
		slices.Reverse(above)
		below := slices.Clone(a[r:])
		m := min(len(above), len(below))
		if slices.Compare(above[:m], below[:m]) == 0 {
			return r
		}
	}
	return 0
}

func reflectionScorePartTwo(a []string) int {
	for r := 1; r < len(a); r++ {
		above := slices.Clone(a[:r])
		slices.Reverse(above)
		below := slices.Clone(a[r:])
		var diff int
		for i := 0; i < len(above) && i < len(below); i++ {
			for j := 0; j < len(above[i]); j++ {
				if above[i][j] != below[i][j] {
					diff++
				}
			}
		}
		if diff == 1 {
			return r
		}
	}
	return 0
}

func min(a int, b int) int {
	if a < b {
		return a
	}
	return b
}
