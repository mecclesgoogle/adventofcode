package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

type Range struct {
	destStart   int
	sourceStart int
	length      int
}

type SeedMap struct {
	source string
	dest   string
	ranges []Range
}

func (s *SeedMap) appendRange(r Range) {
	s.ranges = append(s.ranges, r)
}

func main() {
	file, _ := os.Open("aoc_5.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	scanner.Scan()
	line := scanner.Text()
	seeds := strings.Split(line, " ")[1:]
	seedsPartTwo := make([][]int, 0)
	for i := 0; i < len(seeds)-1; i += 2 {
		start, _ := strconv.Atoi(seeds[i])
		number, _ := strconv.Atoi(seeds[i+1])
		seedsPartTwo = append(seedsPartTwo, []int{start, number})
	}
	maps := make([]*SeedMap, 0)
	var currentMap *SeedMap
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			continue
		}
		if strings.Contains(line, "map:") {
			a := strings.Split(line, " ")[0]
			b := strings.Split(a, "-")
			currentMap = &SeedMap{b[0], b[2], nil}
			maps = append(maps, currentMap)
		} else {

			p := strings.Fields(line)
			a, _ := strconv.Atoi(p[0])
			b, _ := strconv.Atoi(p[1])
			c, _ := strconv.Atoi(p[2])
			currentMap.appendRange(Range{a, b, c})
		}
	}

	partOneResult := math.MaxInt32
	for _, s := range seeds {
		si, _ := strconv.Atoi(s)
		loc := getLocation(si, maps)
		if loc < partOneResult {
			partOneResult = loc
		}
	}
	fmt.Printf("Part 1: %v\n", partOneResult)

	partTwoResult := math.MaxInt32
	for _, s := range seedsPartTwo {
		for l := s[0]; l < s[0]+s[1]; l++ {
			loc := getLocation(l, maps)
			if loc < partTwoResult {
				partTwoResult = loc
			}
		}
	}
	fmt.Printf("Part 2: %v\n", partTwoResult)
}

func getLocation(seed int, seedMap []*SeedMap) int {
	seedLocation := seed
	for _, m := range seedMap {
		for _, r := range m.ranges {
			if seedLocation >= r.sourceStart && seedLocation <= r.sourceStart+r.length-1 {
				seedLocation = seedLocation + r.destStart - r.sourceStart
				break
			}
		}
	}
	return seedLocation
}
