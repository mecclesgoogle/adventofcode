package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strings"
)

type Node struct {
	x    int
	y    int
	pipe rune
}

var NORTH_FROM_SOUTH = "|7FS"
var SOUTH_FROM_NORTH = "|LJS"
var EAST_FROM_WEST = "-J7S"
var WEST_FROM_EAST = "-FLS"

func main() {
	file, _ := os.Open("aoc_10.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	sewer := make(map[int][]Node)
	var r int
	var start Node
	for scanner.Scan() {
		line := scanner.Text()
		row := make([]Node, 0)
		for c, pipe := range line {
			n := Node{r, c, pipe}
			row = append(row, n)
			if pipe == 'S' {
				start = n
			}
		}
		sewer[r] = row
		r++
	}
	path := furthestPipe(start, sewer)
	fmt.Println("Part one", len(path)/2)
	p2 := append(path, start)

	slices.Reverse(p2) // This isn't very deterministic, but works for sample input.

	var t int
	for i := 0; i < len(p2)-1; i++ {
		t += (p2[i].x * p2[i+1].y)
		t -= (p2[i].y * p2[i+1].x)
	}
	a := t / 2
	// https://en.wikipedia.org/wiki/Pick's_theorem#Formula
	// A=i+{\frac {b}{2}}-1
	// i = A - b/2 - 1
	partTwo := a - (len(p2) / 2) + 1
	fmt.Println("Part two", partTwo)
}

func furthestPipe(start Node, sewer map[int][]Node) []Node { // BFS algorithm.
	visited := []Node{}
	queue := []Node{start}
	for len(queue) > 0 {
		next := queue[0]
		queue = queue[1:]
		visited = append(visited, next)

		// South
		if next.x < len(sewer)-1 && strings.ContainsRune(NORTH_FROM_SOUTH, next.pipe) {
			south := sewer[next.x+1][next.y]
			if strings.ContainsRune(SOUTH_FROM_NORTH, south.pipe) {
				if !slices.Contains(visited, south) {
					queue = append(queue, south)
					continue
				}
			}
		}

		// West
		if next.y > 0 && strings.ContainsRune(EAST_FROM_WEST, next.pipe) {
			west := sewer[next.x][next.y-1]
			if strings.ContainsRune(WEST_FROM_EAST, west.pipe) {
				if !slices.Contains(visited, west) {
					queue = append(queue, west)
					continue
				}
			}
		}

		// North
		if next.x > 0 && strings.ContainsRune(SOUTH_FROM_NORTH, next.pipe) {
			north := sewer[next.x-1][next.y]
			if strings.ContainsRune(NORTH_FROM_SOUTH, north.pipe) {
				if !slices.Contains(visited, north) {
					queue = append(queue, north)
					continue
				}
			}
		}

		// East
		if next.y < len(sewer[0])-1 && strings.ContainsRune(WEST_FROM_EAST, next.pipe) {
			east := sewer[next.x][next.y+1]
			if strings.ContainsRune(EAST_FROM_WEST, east.pipe) {
				if !slices.Contains(visited, east) {
					queue = append(queue, east)
					continue
				}
			}
		}

	}
	return visited
}
