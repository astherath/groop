package parser

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strings"
	"time"
)

type Message struct {
	Date   time.Time
	Author string
	Body   string
}

const (
	layoutWhatsapp = "[01/02/06, 03:04:05 PM]"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func ParseDate(date string) (string, error) {

	t, err := time.Parse(layoutWhatsapp, date)
	if err != nil {
		return t.String(), errors.New("invalid date")
	}

	return t.String(), nil
}

func ReadChatFile(pathname string) {
	file, err := os.Open(pathname)
	check(err)
	defer file.Close()

	s := bufio.NewScanner(file)
	for s.Scan() {
		writeMessage(s.Text())
	}
	err = s.Err()
	check(err)
}

func writeMessage(message string) {
	// declaring vars inside statement
	var author string
	var body string

	end := strings.IndexByte(message, ']') + 1
	date := strings.TrimSpace(message[:end])
	message = message[end:]
	end = strings.IndexByte(message, ':')
	if end == -1 {
		author = "System message"
		body = strings.TrimSpace(message)
	} else {
		author = strings.TrimSpace(message[:end])
		body = strings.TrimSpace(message[end+1:])
	}

	fmt.Println("date: ", date, "\nauthor: ", author, "\nbody: ", body)

	// data, _ := json.MarshallIndent(messages, "", " ")
	// _ := ioutil.WriteFile("message_test.json", file, 0644)
}
