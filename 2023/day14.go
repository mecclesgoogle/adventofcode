package main

import (
	"bufio"
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"os"
	"slices"
	"strings"
)

var cache map[string]int

func main() {
	file, _ := os.Open("aoc_14.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var dish Dish
	dish = make([]string, 0)
	for scanner.Scan() {
		dish = append(dish, scanner.Text())
	}
	t := tiltNorth(dish)
	fmt.Println(score(t))
	partTwo(dish)
}

func GetMD5Hash(text string) string {
	hash := md5.Sum([]byte(text))
	return hex.EncodeToString(hash[:])
}

func partTwo(d Dish) {
	numCycles := 1000000000
	cache = make(map[string]int)
	var cycleTo int
	for i := 1; i <= numCycles; i++ {
		d = cycle(d)
		_, ok := cache[d.HashKey()]
		if ok {
			cycleTo = i
			break
		}
		cache[d.HashKey()] = i
	}
	cyclesRemaining := numCycles - cycleTo
	cyclesRemaining = cyclesRemaining % (cycleTo - cache[d.HashKey()])
	j := 0
	for j < cyclesRemaining {
		d = cycle(d)
		j++
	}
	fmt.Println(score(d))

}

type Dish []string

func (d Dish) HashKey() string {
	return GetMD5Hash(strings.Join(d, ""))
}

func cycle(dish Dish) Dish {
	dish = tiltNorth(dish)
	dish = tiltWest(dish)
	dish = tiltSouth(dish)
	dish = tiltEast(dish)
	return dish
}

func score(dish []string) int {
	numRows := len(dish)
	var score int
	for i, v := range dish {
		for _, v2 := range v {
			if v2 == 'O' {
				score += numRows - i
			}
		}
	}
	return score
}

func printDish(dish []string) {
	for _, v := range dish {
		fmt.Println(v)

	}
}

func tiltNorth(dish []string) []string {
	t := transpose(dish)
	t = pushRocksLeft(t)
	t = transpose(t)
	return t
}

func pushRocksLeft(dish []string) []string {
	return pushRocks(dish, true)
}

func pushRocksRight(dish []string) []string {
	return pushRocks(dish, false)
}

func pushRocks(dish []string, reverse bool) []string {
	for i, v := range dish {
		var n string
		s := strings.Split(v, "#")
		for i2, v2 := range s {
			p := StringToSlice(v2)
			slices.Sort(p)
			if reverse {
				slices.Reverse(p)
			}

			n += strings.Join(p, "")
			if i2 < len(s)-1 {
				n += "#"
			}
		}
		dish[i] = n
	}
	return dish
}

func tiltWest(dish []string) []string {
	return pushRocksLeft(dish)
}

func tiltSouth(dish []string) []string {
	t := transposeOppositeDiagonal(dish)
	t = pushRocksLeft(t)
	t = transposeOppositeDiagonal(t)
	return t
}

func tiltEast(dish []string) []string {
	return pushRocksRight(dish)
}

func StringToSlice(dish string) []string {
	result := make([]string, len(dish))
	for i, v := range dish {
		result[i] = string(v)
	}
	return result
}

func transpose(dish []string) []string {
	result := make([]string, 0)
	for c := 0; c < len(dish[0]); c++ {
		var row string
		for r := 0; r < len(dish); r++ {
			row += string(dish[r][c])
		}
		result = append(result, row)
	}
	return result
}

func transposeOppositeDiagonal(dish []string) []string {
	result := make([]string, 0)
	for c := len(dish[0]) - 1; c >= 0; c-- {
		var row string
		for r := len(dish) - 1; r >= 0; r-- {
			row += string(dish[r][c])
		}
		result = append(result, row)
	}
	return result
}
