package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Problem struct {
	sequence string
	rules    []int
}

func cacheKey(sequence string, rules []int) string {
	key := sequence
	for _, v := range rules {
		key += strconv.Itoa(v)
	}
	return key
}

var cache map[string]int

func len_0[T any](a []T) int {
	if len(a) == 0 {
		return 1
	} else {
		return 0
	}
}

func count(sequence string, rules []int) int {
	if sequence == "" { // End
		return len_0(rules)
	}
	if len(rules) == 0 {
		if strings.ContainsRune(sequence, '#') {
			return 0
		}
		return 1
	}

	cacheKey := cacheKey(sequence, rules)
	val, ok := cache[cacheKey]
	if ok {
		return val
	}

	var result int
	nextRune := rune(sequence[0])
	nextNum := rules[0]
	if nextRune == '.' || nextRune == '?' {
		result += count(sequence[1:], rules)
	}
	if nextRune == '#' || nextRune == '?' { // start block
		if nextNum == len(sequence) && !strings.Contains(sequence[:nextNum], ".") {
			if len(rules) == 1 {
				result += 1
			} else {
				return 0
			}
		} else if nextNum <= len(sequence) && !strings.Contains(sequence[:nextNum], ".") &&
			(nextNum == len(sequence) || string(sequence[nextNum]) != "#") {
			result += count(sequence[nextNum+1:], rules[1:])
		} else {
			result += 0
		}
	}
	cache[cacheKey] = result
	return result
}

func main() {
	file, _ := os.Open("aoc_12.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var p []Problem
	for scanner.Scan() {
		line := scanner.Text()
		a := strings.Fields(line)
		b := strings.Split(a[1], ",")
		c := make([]int, len(b))
		for i, v := range b {
			c[i], _ = strconv.Atoi(v)
		}
		p = append(p, Problem{a[0], c})

	}
	var partOne, partTwo int
	for _, p2 := range p {
		cache = make(map[string]int)
		partOne += count(p2.sequence, p2.rules)
		partTwo += count(join(p2.sequence, "?", 5), repeatSlice(p2.rules, 5))
	}
	fmt.Println(partOne)
	fmt.Println(partTwo)
}

func join(s string, p string, n int) string {
	var r string
	for i := 0; i < n; i++ {
		r += s
		if i != 4 {
			r += p
		}
	}
	return r
}

func repeatSlice(s []int, n int) []int {
	result := append([]int{}, s...)
	for i := 1; i < n; i++ {
		result = append(result, s...)
	}
	return result
}
