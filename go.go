package main

import "fmt"

func task(char string) {
   fmt.Println(char)
}

func main() {
   //go task("this the char string to be printed")
   task("a random string")
   fmt.Println()
}