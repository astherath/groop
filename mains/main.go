package main

import (
	"fmt"

	"github.com/astherath/parser"
)

func main() {
	date := "[01/02/06, 03:04:05 PM]"
	fmt.Println(parser.Parse(date))

}
