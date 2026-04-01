package main

import (
	"fmt"
)

// Функція, що повертає рядок
func greet(name string) string {
	return "Привіт, " + name + "!"
}

// Функція для обчислення факторіала
func factorial(n int) int {
	if n <= 1 {
		return 1
	}
	return n * factorial(n-1)
}

func main() {
	// Виклик функцій
	message := greet("Користувач")
	fmt.Println(message)

	result := factorial(5)
	fmt.Printf("Факторіал 5 дорівнює: %d\n", result)
}