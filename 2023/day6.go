package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Race struct {
	time     int
	distance int
}

func main() {
	file, _ := os.Open("aoc_6.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)

	scanner.Scan()
	line := scanner.Text()
	timeLine := line
	scanner.Scan()
	line = scanner.Text()
	distanceLine := line

	times := strings.Fields(timeLine)[1:]
	distances := strings.Fields(distanceLine)[1:]

	var partOneTotal int

	for i := 0; i < len(times); i++ {
		time, _ := strconv.Atoi(times[i])
		distance, _ := strconv.Atoi(distances[i])
		if i == 0 {
			partOneTotal = calcScore(time, distance+1)
		} else {
			partOneTotal *= calcScore(time, distance+1)
		}

	}

	fmt.Printf("Part 1: %v\n", partOneTotal)

	partTwoTime := strings.ReplaceAll(timeLine, " ", "")
	partTwoTime = strings.Split(partTwoTime, ":")[1]
	partTwoDistance := strings.ReplaceAll(distanceLine, " ", "")
	partTwoDistance = strings.Split(partTwoDistance, ":")[1]
	var partTwoTotal int
	p2tInt, _ := strconv.Atoi(partTwoTime)
	p2tDst, _ := strconv.Atoi(partTwoDistance)
	partTwoTotal = calcScore(p2tInt, p2tDst+1)

	fmt.Printf("Part 2: %v\n", partTwoTotal)

}

func calcScore(time int, minDistance int) int {
	var score int
	for speed := 0; speed <= time; speed++ {
		timeLeft := time - speed
		distance := speed * timeLeft
		if distance >= minDistance {
			score++
		}
	}

	return score
}
