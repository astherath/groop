package parser

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

type Message struct {
	Date   string
	Author string
	Body   string
}

const (
	debug           = false
	layoutWhatsapp  = "[01/02/06, 03:04:05 PM]"
	layoutWhatsapp1 = "[01/02/06, 3:04:05 PM]"
	layoutISO       = "2006-01-02T15:04:05-0700"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func ReadChatFile(pathname string) {
	start := time.Now()
	fmt.Println("Starting to process file now ...")

	file, err := os.Open(pathname)
	check(err)
	defer file.Close()

	var messages []Message
	i := 0

	s := bufio.NewScanner(file)
	s.Split(crunchSplitFunc)
	for s.Scan() {
		fmt.Println("have written: ", i, " lines of data so far")
		message, eof := parseraw_message(s.Text())
		if !eof {
			i++
			messages = append(messages, message)
		}
	}
	err = s.Err()
	check(err)

	writeMessage(messages)

	elapsed := time.Since(start)
	fmt.Println("Formatting the GC file took: ", elapsed)
}

func writeMessage(messages []Message) {
	data, _ := json.MarshalIndent(messages, "", " ")
	_ = ioutil.WriteFile("message_test.json", data, 0644)
}

func parseraw_message(raw_message string) (Message, bool) {
	// declaring vars inside statement
	var author string
	var body string
	end := strings.IndexByte(raw_message, ']') + 1
	if debug {
		fmt.Println("end1: ", end)
	}
	raw_date := strings.TrimSpace(raw_message[:end])

	raw_message = raw_message[end:]
	end = strings.IndexByte(raw_message, ':')
	if debug {
		fmt.Println("end2: ", end)
	}
	if end == -1 {
		// TODO: handle different types of system messages
		author = "System message"
		body = strings.TrimSpace(raw_message)
	} else {
		author = strings.TrimSpace(raw_message[:end])
		body = strings.TrimSpace(raw_message[end+1:])
	}

	if debug {
		fmt.Printf("author: %s, body: %s\n", author, body)
	}

	date, err2 := parseDate(raw_date)
	// check(err2)

	// create message object
	message := Message{date, author, body}
	if err2 != nil {
		return message, true
	}
	if debug {
		fmt.Println("message: ", message)
	}

	return message, false
}

func parseDate(date string) (string, error) {

	t, err := time.Parse(layoutWhatsapp, date)
	if err != nil {
		t2, err2 := time.Parse(layoutWhatsapp1, date)
		if err2 != nil {
			if debug {
				fmt.Println("date: ", date, "original error: ", err)
			}
			return t.String(), err
		}
		t = t2
	}
	isoTime := t.Format(layoutISO)

	return isoTime, nil
}

func crunchSplitFunc(data []byte, atEOF bool) (advance int, token []byte, err error) {

	// Return nothing if at end of file and no data passed
	if atEOF && len(data) == 0 {
		return 0, nil, nil
	}

	if i := bytes.IndexByte(data, '\r'); i >= 0 {
		// We have a full newline-terminated line.
		return i + 1, data[0:i], nil
	}

	// If at end of file with data return the data
	if atEOF {
		return len(data), data, nil
	}

	return 0, nil, nil
}
