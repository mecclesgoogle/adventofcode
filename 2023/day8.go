package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
)

type Node struct {
	loc string
	l   string
	r   string
}

func FindNode(nodes []Node, loc string) Node {
	for _, n := range nodes {
		if n.loc == loc {
			return n
		}
	}
	return nodes[0]
}

func main() {
	file, _ := os.Open("aoc_8.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	scanner.Scan()
	directions := scanner.Text()

	nodes := make([]Node, 0)
	scanner.Scan()
	for scanner.Scan() {
		line := scanner.Text()
		re := regexp.MustCompile(`[A-Z0-9]{3}`)
		m := re.FindAllString(line, -1)
		n := Node{m[0], m[1], m[2]}
		nodes = append(nodes, n)
	}
	var partOne int
	var loc Node
	for _, n := range nodes {
		if n.loc == "AAA" {
			loc = n
			break
		}
	}
	for loc.loc != "ZZZ" {
		d := directions[partOne%len(directions)]
		if d == 'L' {
			loc = FindNode(nodes, loc.l)
		}
		if d == 'R' {
			loc = FindNode(nodes, loc.r)
		}
		partOne++
	}
	fmt.Println("Part one:", partOne)

	locs := make([]Node, 0)
	for _, n := range nodes {
		if n.loc[2] == 'A' {
			locs = append(locs, n)
		}
	}

	stepsPerLoc := make([]int, len(locs))
	for i, n := range locs {
		var numSteps int
		for n.loc[2] != 'Z' {
			d := directions[numSteps%len(directions)]
			if d == 'L' {
				n = FindNode(nodes, n.l)
			}
			if d == 'R' {
				n = FindNode(nodes, n.r)
			}
			numSteps++
		}
		stepsPerLoc[i] = numSteps
	}
	fmt.Println("Part two:", lcmList(stepsPerLoc))
}

// Thanks BARD :)
func gcd(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func lcm(a, b int) int {
	return a * b / gcd(a, b)
}

func lcmList(numbers []int) int {
	lcmValue := 1
	for _, number := range numbers {
		lcmValue = lcm(lcmValue, number)
	}
	return lcmValue
}
