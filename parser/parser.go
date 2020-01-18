package parser

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"os"
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
	defer func() {
		if err = file.Close(); err != nil {
			log.Fatal(err)
		}
	}()

	s := bufio.NewScanner(file)
	for s.Scan() {
		fmt.Println(s.Text())
	}
	err = s.Err()
	check(err)
}

func writeMessage(messages []Message) {
	data, _ := json.MarshallIndent(messages, "", " ")
	_ := ioutil.WriteFile("message_test.json", file, 0644)
}



