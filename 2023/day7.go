package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Hand struct {
	hand string
	bid  int
}

var CARD_VALUES = map[rune]int{
	'A': 14,
	'K': 13,
	'Q': 12,
	'J': 11,
	'T': 10,
	'9': 9,
	'8': 8,
	'7': 7,
	'6': 6,
	'5': 5,
	'4': 4,
	'3': 3,
	'2': 2,
}

const ( // lower wins
	FIVE_OF_A_KIND  = iota // 0
	FOUR_OF_A_KIND  = iota // 1
	FULL_HOUSE      = iota // 2
	THREE_OF_A_KIND = iota // 3
	TWO_PAIR        = iota // 4
	ONE_PAIR        = iota // 5
	HIGH_CARD       = iota // 6

)

func (h Hand) ScorePart2() int {
	numJacks := strings.Count(h.hand, "J")
	if numJacks == 5 {
		// JJJJJ
		return FIVE_OF_A_KIND
	}
	if numJacks == 4 {
		// JJXJJ
		return FIVE_OF_A_KIND
	}
	n := countUniqueRunes(h.hand) - 1
	if numJacks == 3 {
		if n == 2 {
			// JJJXY
			return FOUR_OF_A_KIND
		}
		// JJJXX
		return FIVE_OF_A_KIND
	}
	if numJacks == 2 {
		if n == 3 {
			// JJXYZ
			return THREE_OF_A_KIND
		}
		if n == 2 {
			// JJXXY
			return FOUR_OF_A_KIND
		}
		// JJXXX
		return FIVE_OF_A_KIND
	}
	if numJacks == 1 {
		if n == 4 {
			// JXYZA
			return ONE_PAIR
		}
		if n == 3 {
			// JXYYZ
			return THREE_OF_A_KIND
		}
		if n == 2 {
			_, c := getMostCommonRune(h.hand)
			if c == 3 {
				// JXXXY
				return FOUR_OF_A_KIND
			}
			// JXXYY
			return FULL_HOUSE
			// Could be FOUR_OF_A_KIND
		}
		// JXXXX
		return FIVE_OF_A_KIND
	}
	return h.Score()
}

func countUniqueRunes(text string) int {
	runeCount := map[rune]bool{}
	for _, r := range text {
		runeCount[r] = true
	}
	return len(runeCount)
}

func getMostCommonRune(text string) (rune, int) {
	runeCounts := map[rune]int{}
	for _, r := range text {
		runeCounts[r]++
	}

	mostCommonRune := rune(0)
	mostCommonCount := 0
	for r, count := range runeCounts {
		if count > mostCommonCount {
			mostCommonRune = r
			mostCommonCount = count
		}
	}

	return mostCommonRune, mostCommonCount
}

func splitRunes(hand string) map[rune]int {
	m := make(map[rune]int)
	for _, c := range hand {
		_, ok := m[c]
		if ok {
			m[c] += 1
		} else {
			m[c] = 1
		}
	}
	return m
}

func (h Hand) Score() int {
	m := splitRunes(h.hand)
	if len(m) == 5 {
		return HIGH_CARD
	}
	if len(m) == 4 {
		return ONE_PAIR
	}
	if len(m) == 3 {
		for _, v := range m {
			if v == 3 {
				return THREE_OF_A_KIND
			}
		}
		return TWO_PAIR
	}
	if len(m) == 2 {
		for _, v := range m {
			if v == 1 || v == 4 {
				return FOUR_OF_A_KIND
			}
		}
		return FULL_HOUSE
	}
	return FIVE_OF_A_KIND
}

func CompareCards(c1 rune, c2 rune) int {
	return CARD_VALUES[c2] - CARD_VALUES[c1]
}

func (h Hand) CompareHand(other Hand, part int) int {
	var score int
	var otherScore int
	if part == 1 {
		score = h.Score()
		otherScore = other.Score()
	}
	if part == 2 {
		score = h.ScorePart2()
		otherScore = other.ScorePart2()
	}
	if score < otherScore {
		return -1
	}
	if score > otherScore {
		return 1
	}
	for i := 0; i < 5; i++ {
		diff := CompareCards(rune(h.hand[i]), rune(other.hand[i]))
		if diff != 0 {
			return diff
		}
	}
	return 0
}

func main() {
	file, _ := os.Open("aoc_7.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	hands := make([]Hand, 0)
	for scanner.Scan() {
		line := scanner.Text()
		f := strings.Fields(line)
		bid, _ := strconv.Atoi(f[1])
		hand := Hand{f[0], bid}
		hands = append(hands, hand)
	}

	hands = BubbleSort(hands, 1)

	var partOneTotal int
	for i, h := range hands {
		if i == 0 {
			partOneTotal = h.bid
			continue
		}
		partOneTotal += h.bid * (i + 1)
	}
	fmt.Println("Part one total:", partOneTotal)

	CARD_VALUES['J'] = -1
	hands = BubbleSort(hands, 2)

	var partTwoTotal int
	for i, h := range hands {
		if i == 0 {
			partTwoTotal = h.bid
			continue
		}
		partTwoTotal += h.bid * (i + 1)
	}
	fmt.Println("Part two total:", partTwoTotal)
}

func BubbleSort(hands []Hand, part int) []Hand {
	for i := 0; i < len(hands)-1; i++ {
		for j := 0; j < len(hands)-i-1; j++ {
			if hands[j].CompareHand(hands[j+1], part) < 0 {
				hands[j], hands[j+1] = hands[j+1], hands[j]

			}
		}
	}
	return hands
}
