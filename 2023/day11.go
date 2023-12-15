package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"slices"
)

var GALAXY = '#'
var SPACE = '.'

type Loc struct {
	x int
	y int
}

type Universe struct {
	nodes        [][]rune
	expandedRows []int
	expandedCols []int
}

func main() {
	file, _ := os.Open("aoc_11.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var r int
	var universe Universe
	for scanner.Scan() {
		line := scanner.Text()
		row := make([]rune, 0)
		g := false
		for _, node := range line {
			row = append(row, node)
			if node == GALAXY {
				g = true
			}
		}
		universe.nodes = append(universe.nodes, row)
		if !g {
			universe.expandedRows = append(universe.expandedRows, r)
		}
		r++
	}
	universe.expandedCols = addColumns(universe)

	galaxies := findGalaxies(universe.nodes)

	var partOne int
	var partTwo int
	for i := 0; i < len(galaxies)-1; i++ {
		p1 := galaxies[i]
		for j := i + 1; j < len(galaxies); j++ {
			p2 := galaxies[j]
			partOne += distance(universe, p1, p2, 1)
			partTwo += distance(universe, p1, p2, 1_000_000-1)
		}
	}
	fmt.Println("Part 1:", partOne)
	fmt.Println("Part 2:", partTwo)
}

func distance(u Universe, p1 Loc, p2 Loc, x int) int {
	var extra int

	if p1.x < p2.x {
		for r := p1.x; r < p2.x; r++ {
			if slices.Contains(u.expandedRows, r) {
				extra += x
			}
		}
	}
	if p1.x > p2.x {
		for r := p1.x; r > p2.x; r-- {
			if slices.Contains(u.expandedRows, r) {
				extra += x
			}
		}
	}
	if p1.y < p2.y {
		for c := p1.y; c < p2.y; c++ {
			if slices.Contains(u.expandedCols, c) {
				extra += x
			}
		}
	}
	if p1.y > p2.y {
		for c := p1.y; c > p2.y; c-- {
			if slices.Contains(u.expandedCols, c) {
				extra += x
			}
		}
	}

	return abs(p1.x-p2.x) + abs(p1.y-p2.y) + extra
}

func abs(x int) int {
	return int(math.Abs(float64(x)))
}

func addColumns(universe Universe) []int {
	var expandedCols []int
	for c := 0; c < len(universe.nodes[0]); c++ {
		found := false
		for r := 0; r < len(universe.nodes); r++ {
			if universe.nodes[r][c] == GALAXY {
				found = true
				break
			}
		}
		if !found { // Necessary?
			expandedCols = append(expandedCols, c)
		}
	}
	return expandedCols
}

func findGalaxies(universe [][]rune) []Loc {
	galaxies := make([]Loc, 0)
	for r := 0; r < len(universe); r++ {
		for c := 0; c < len(universe[0]); c++ {
			if universe[r][c] == GALAXY {
				galaxies = append(galaxies, Loc{r, c})
			}
		}
	}
	return galaxies
}
