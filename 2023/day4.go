package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strings"
)

type Card struct {
	number  int
	winners int
	copies  int
}

func score(winners []string, mycards []string) (int, float64) {
	var numWinners int
	for _, card := range mycards {
		for _, winner := range winners {
			if card == winner {
				numWinners++
			}
		}
	}
	if numWinners == 0 {
		return 0, 0
	}
	return numWinners, math.Pow(float64(2), float64(numWinners-1))
}

func main() {
	file, _ := os.Open("aoc_4.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var partOneTotal float64
	var partTwoTotal int
	cards := make([]Card, 0)
	index := 1
	for scanner.Scan() {
		line := scanner.Text()
		x := strings.Split(line, ":")[1]
		parts := strings.Split(x, "|")
		winners := strings.TrimSpace(parts[0])
		mycards := strings.TrimSpace(parts[1])
		numWinners, gameScore := score(strings.Fields(winners), strings.Fields(mycards))
		partOneTotal += gameScore
		// part 2
		cards = append(cards, Card{index, numWinners, 1})
		index++
	}
	fmt.Printf("Part 1: %f\n", partOneTotal)
	for _, c := range cards {
		for i := c.number + 1; i < c.winners+c.number+1; i++ {
			if i <= len(cards) {
				cards[i-1].copies += c.copies
			}
		}
	}
	for _, c := range cards {
		partTwoTotal += c.copies
	}
	fmt.Printf("Part 2: %v\n", partTwoTotal)
}
