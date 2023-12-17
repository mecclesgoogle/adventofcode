package main

import (
	"fmt"
	"slices"
)

func main() {
	// reverse()
	// search()
	compare()
}

func search() {
	a := []int{1, 2, 3, 4, 5}
	x, y := slices.BinarySearch(a, 5)
	fmt.Println(x, y)
}

func reverse() {
	a := []int{1, 2, 3, 4, 5}

	b := a[1:3]
	c := slices.Clone(b)
	fmt.Println(b) // [2 3]
	fmt.Println(c) // [2 3]

	slices.Reverse(a)
	fmt.Println(a) // [5 4 3 2 1]

	fmt.Println(b) // [4 3]
	fmt.Println(c) // [2 3]
}

func compare() {
	a := []int{1, 2, 3, 4, 5}
	b := []int{1, 2, 1, 9, 5}
	diff := slices.CompareFunc(a, b, func(a int, b int) int {
		if a == b {
			return 0
		} else {
			return 1
		}
	})
	fmt.Println("diff", diff)

}
