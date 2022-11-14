package utils

import (
	"log"
	"regexp"
	"strings"
	"time"
)

func TrackTime(start time.Time) {
	elapsed := time.Since(start)
	log.Printf("took %s", elapsed)
}

func RemoveSupText(text, replace string) string {
	reg := regexp.MustCompile(`[\(\[].*?[\)\]]`)
	return strings.TrimSpace(reg.ReplaceAllString(text, replace))
}

func SetDelimiter(text, delimiter string) string {
	reg := regexp.MustCompile(`\s*,+\s*`)
	return reg.ReplaceAllLiteralString(reg.ReplaceAllString(text, delimiter), delimiter)
}

func RemoveFromSlice[T comparable](slice []T, remove T) []T {
	var newSlice []T
	for _, elem := range slice {
		if elem != remove {
			newSlice = append(newSlice, elem)
		}
	}
	return newSlice
}

func RemoveFromSliceRegex(slice []string, remove string, keepInsted bool) []string {
	var newSlice []string
	regExp := regexp.MustCompile(remove)

	for _, elem := range slice {
		if regExp.MatchString(elem) == keepInsted {
			newSlice = append(newSlice, elem)
		}
	}

	return newSlice
}

func RemoveDuplicates[T comparable](slice []T) []T {
	var set map[T]struct{} = map[T]struct{}{}
	var ok bool
	var newSlice []T

	for _, elem := range slice {
		if _, ok = set[elem]; !ok {
			set[elem] = struct{}{}
			newSlice = append(newSlice, elem)
		}
	}

	return newSlice
}
