package parser

import (
	"errors"
	"time"
)

const (
	layoutWhatsapp = "[01/02/06, 03:04:05 PM]"
)

func Parse(date string) (string, error) {

	t, err := time.Parse(layoutWhatsapp, date)
	if err != nil {
		return t.String(), errors.New("invalid date")
	}

	return t.String(), nil
}
