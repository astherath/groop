package main

import (
	"github.com/astherath/parser"
	"os"
)

func main() {
	// read pathname from command line
	pathname := os.Args[1]

	// this handles all of the reading and parsing
	parser.ReadChatFile(pathname)
}
