package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
)

type Coords struct {
	x int
	y int
}

type State struct {
	x  int
	y  int
	dx int
	dy int
}

// FIFO Queue
type Queue[T interface{}] []T

func (q *Queue[T]) Enqueue(value T) {
	*q = append(*q, value)
}

func (q *Queue[T]) PopEnd() (T, bool) {
	if len(*q) == 0 {
		var zero T
		return zero, false
	}
	value := (*q)[len(*q)-1]
	*q = slices.Delete(*q, len(*q)-1, len(*q))
	return value, true
}

func (q *Queue[T]) IsEmpty() bool {
	return len(*q) == 0
}

func main() {
	file, _ := os.Open("aoc_16.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	cave := make([]string, 0)
	for scanner.Scan() {
		line := scanner.Text()
		cave = append(cave, line)
	}
	fmt.Println(energy(cave, State{0, -1, 0, 1}))

	var partTwo int
	for r := 0; r < len(cave); r++ {
		partTwo = max(
			partTwo,
			energy(cave, State{r, -1, 0, -1}),
			energy(cave, State{r, len(cave[0]), 0, -1}))
	}
	for c := 0; c < len(cave[0]); c++ {
		partTwo = max(
			partTwo,
			energy(cave, State{-1, c, 1, 0}),
			energy(cave, State{len(cave), c, -1, 0}))
	}
	fmt.Println(partTwo)
}

func energy(cave []string, initialState State) int {
	queue := Queue[State]{initialState}
	energized := make(map[State]bool)

	for !queue.IsEmpty() {
		state, _ := queue.PopEnd()
		x := state.x + state.dx
		y := state.y + state.dy

		// Check in bounds
		if x < 0 || x >= len(cave) || y < 0 || y >= len(cave[0]) {
			continue
		}

		// Make move
		symbol := rune(cave[x][y])

		if symbol == '.' || (state.dx == 0 && symbol == '-') || (state.dy == 0 && symbol == '|') {
			nextState := State{x, y, state.dx, state.dy}
			_, ok := energized[nextState]
			if !ok {
				queue.Enqueue(nextState)
				energized[nextState] = true
			}
		} else if symbol == '/' {
			nextState := State{x, y, -state.dy, -state.dx}
			_, ok := energized[nextState]
			if !ok {
				queue.Enqueue(nextState)
				energized[nextState] = true
			}
		} else if symbol == '\\' {
			nextState := State{x, y, state.dy, state.dx}
			_, ok := energized[nextState]
			if !ok {
				queue.Enqueue(nextState)
				energized[nextState] = true
			}
		} else {
			if symbol == '-' {
				nextState := State{x, y, 0, -1}
				nextState2 := State{x, y, 0, 1}
				_, ok := energized[nextState]
				if !ok {
					queue.Enqueue(nextState)
					energized[nextState] = true
				}
				_, ok = energized[nextState2]
				if !ok {
					queue.Enqueue(nextState2)
					energized[nextState2] = true
				}
			}
			if symbol == '|' {
				nextState := State{x, y, -1, 0}
				nextState2 := State{x, y, 1, 0}
				_, ok := energized[nextState]
				if !ok {
					queue.Enqueue(nextState)
					energized[nextState] = true
				}
				_, ok = energized[nextState2]
				if !ok {
					queue.Enqueue(nextState2)
					energized[nextState2] = true
				}
			}
		}
	}

	m := make(map[Coords]bool)
	for k, _ := range energized {
		m[Coords{k.x, k.y}] = true
	}
	return len(m)
}
