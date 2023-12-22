package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	file, _ := os.Open("aoc_15.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	scanner.Scan()
	line := scanner.Text()

	p := strings.Split(line, ",")

	var partOne int
	for _, v := range p {
		partOne += hash(v)
	}
	fmt.Println(partOne)

	boxes := make([]Box, 256)
	for _, v := range p {
		if strings.Contains(v, "-") {
			p := strings.Split(v, "-")
			label := p[0]
			hash := hash(label)
			boxes[hash].removeLens(Lens{label, -1})
		}
		if strings.Contains(v, "=") {
			p := strings.Split(v, "=")
			hash := hash(p[0])
			val := p[1]
			length, _ := strconv.Atoi(val)
			lens := Lens{p[0], length}
			if len(boxes[hash].lenses) == 0 {
				boxes[hash] = Box{[]Lens{lens}}
			} else {
				boxes[hash].addLens(lens)
			}
		}
	}
	var partTwo int
	for i, b := range boxes {
		for i2, l := range b.lenses {
			partTwo += (i + 1) * (i2 + 1) * l.focal_length
		}
	}
	fmt.Println(partTwo)
}

func printBoxes(boxes []Box) {
	for i, b := range boxes {
		if len(b.lenses) > 0 {
			fmt.Println("box", i, b)

		}
	}
}

type Lens struct {
	label        string
	focal_length int
}

type Box struct {
	lenses []Lens
}

func (b *Box) addLens(l Lens) {
	for i, l2 := range b.lenses {
		if l.label == l2.label {
			b.lenses[i] = l
			return
		}
	}

	b.lenses = append(b.lenses, l)
}

func (b *Box) removeLens(l Lens) {
	newSlice := make([]Lens, 0)
	for _, l2 := range b.lenses {
		if l.label != l2.label {
			newSlice = append(newSlice, l2)
		}
	}
	b.lenses = newSlice
}

func hash(s string) int {
	var hash int
	for _, c := range s {
		hash += int(c)
		hash *= 17
		hash %= 256
	}
	return hash
}
