package main

import (
	"github.com/astherath/parser"
	"fmt"
	"os"
)

func main() {
	// read pathname from command line
	pathname := os.Args[1]

	// this handles all of the reading and parsing
	parser.ReadChatFile(pathname)
	// now delete txt file
	err := os.Remove(pathname)
	if err != nil {
		fmt.Println("Error deleting file")
		panic(err)
	}
}
