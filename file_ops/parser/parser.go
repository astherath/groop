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

var pathname string = ""

type Message struct {
	Date   string
	Author string
	Body   string
}

const (
	debug           = false
	layoutWhatsapp  = "[01/02/06, 03:04:05 PM]"
	layoutWhatsapp1 = "[01/02/06, 3:04:05 PM]"
	layoutWhatsapp2 = "[01/02/06, 15:04:05]"
	layoutWhatsapp3 = "[01/02/06, 15:04 05]"
	layoutISO       = "2006-01-02T15:04:05-0700"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func ReadChatFile(path string) {
	pathname = path
	file, err := os.Open(pathname)
	check(err)
	defer file.Close()

	var messages []Message
	i := 0

	s := bufio.NewScanner(file)
	s.Split(crunchSplitFunc)
	for s.Scan() {
		message, eof := parseraw_message(s.Text())
		if !eof {
			messages = append(messages, message)
			i++
		}
	}
	err = s.Err()
	check(err)

	writeMessage(messages)

}

func writeMessage(messages []Message) {
	data, _ := json.MarshalIndent(messages, "", " ")
	_ = ioutil.WriteFile((pathname + ".json"), data, 0644)
}

func parseraw_message(raw_message string) (Message, bool) {
	// check for EOF
	if len(raw_message) == 0 {
		return Message{"", "", ""}, true
	}
	// declaring vars inside statement
	var author string
	var body string
	end := strings.IndexByte(raw_message, ']') + 1
	if debug {
		fmt.Println("end1: ", end)
	}
	if end == 0 {
		return Message{"", "", ""}, true
	}
	raw_date := strings.TrimSpace(raw_message[:end])
	raw_message = raw_message[end:]

	sysMessage, newMessage := classifySystemMessage(strings.TrimSpace(raw_message))
	if debug {
		fmt.Println("sysmes: ", sysMessage, "\nnewMess: ", newMessage, "\nraw_mess: ", raw_message)
	}
	if sysMessage {
		author = "System message"
		body = newMessage
	} else {
		end = strings.IndexByte(raw_message, ':')
		if debug {
			fmt.Println("end2: ", end)
		}
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

func classifySystemMessage(message string) (bool, string) {
	removed := len(strings.Split(message, " ")) == 3 &&
		strings.Contains(message, " removed ")
	added := len(strings.Split(message, " ")) == 3 &&
		(strings.Contains(message, " added ") ||
		strings.Contains(message, " was added")) ||
		strings.Contains(message, "You were added") ||
		strings.Contains(message, " added ")
	left := len(strings.Split(message, " ")) == 2 &&
		strings.Contains(message, " left")
	image := strings.Contains(message, "image omitted")
	audio := strings.Contains(message, "audio omitted")
	video := strings.Contains(message, "video omitted")
	created := strings.Contains(message, "You created group") || strings.Contains(message, "created this group")
	encryption := strings.Contains(message, "Messages to this group are now secured with end-to-end encryption")
	misc := strings.Contains(message, "deleted the group description")

	if debug {
		fmt.Println("len mess: ", len(strings.Split(message, " ")))
		fmt.Println("rem?: ", strings.Contains(message, " removed "))
		fmt.Println("add?: ", strings.Contains(message, " added "))
		fmt.Println("left?: ", strings.Contains(message, " left"))
		fmt.Println("created?: ", created)
	}
	sysMessage := strings.Contains(message, "changed the subject to") ||
		strings.Contains(message, "You're now an admin") ||
		strings.Contains(message, "changed this group's icon") ||
		strings.Contains(message, "changed the group description") ||
		strings.Contains(message, "deleted this group's icon") ||
		strings.Contains(message, "changed their phone number to a new number. Tap to message or add the new number.") || misc ||
		removed || added || left || image || audio || video || created || encryption

	if sysMessage {
		return true, message
	} else {
		return false, message
	}
}

func parseDate(date string) (string, error) {
	day_date := strings.Split(date[1:strings.Index(date, ",")], "/")
	for i, d := range day_date {
		if len(d) == 1 {
			day_date[i] = "0" + d
		}
	}
	time_date := strings.Split(date[strings.Index(date, ",")+2:len(date)-4], ":")
	for i, d := range time_date {
		if len(d) == 1 {
			time_date[i] = "0" + d
		}
	}
	day_date_string := strings.Join(day_date, "/")
	time_date_string := strings.Join(time_date, ":")
	date = "[" + day_date_string + ", " + time_date_string + " " + date[len(date)-3:]
	if debug {
		fmt.Println("\ndate: ", date)
	}
	t, err := time.Parse(layoutWhatsapp, date)
	// check(err)
	if err != nil {
		if debug {
			fmt.Println("error with first parse, moving to second parser")
			fmt.Println("error", err)
		}
		t2, err2 := time.Parse(layoutWhatsapp2, date)
		if err2 != nil {
			if debug {
				fmt.Println("date: ", date, "original error: ", err, "new err: ", err2)
			}
			t3, err3 := time.Parse(layoutWhatsapp3, date)
			if err3 != nil {
				return t.String(), err
			}
			t2 = t3
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
