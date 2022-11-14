package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/url"
	"os"
	"sort"
	"time"

	"github.com/A-NGJ/socialgraphs2022/scraper"
	"github.com/A-NGJ/socialgraphs2022/utils"
)

func main() {
	var characters []scraper.Character
	var pages []scraper.Page

	jsonFile, err := os.Open("../data/pages.json")
	if err != nil {
		log.Fatal(err)
	}
	defer jsonFile.Close()

	jsonByte, err := io.ReadAll(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	var result map[string]interface{}
	json.Unmarshal(jsonByte, &result)
	for title, url := range result {
		pages = append(pages, scraper.Page{
			Title: title,
			Url:   url.(string),
		})
	}
	sort.Slice(pages, func(a, b int) bool {
		return pages[a].Title < pages[b].Title
	})

	defer utils.TrackTime(time.Now())
	for i := 0; i < len(pages); i = i + 100 {
		var scrapedChars []scraper.Character

		var end int = i + 100
		if i+100 > len(pages) {
			end = len(pages)
		}
		fmt.Printf("\rScraping %d characters", end)
		scrapedChars, err = scraper.Scrape(pages[i:end])
		if err != nil {
			log.Fatal(err)
		}
		characters = append(characters, scrapedChars...)

		for _, char := range scrapedChars {
			charJson, err := json.MarshalIndent(char, "", " ")
			if err != nil {
				log.Printf("WARN: could not marshal %s\n", char.Name)
				continue
			}
			err = os.WriteFile("data/"+url.QueryEscape(char.Name)+".json", charJson, 0644)
			if err != nil {
				log.Printf("WARN: could not save %s.json", char.Name)
			}
		}
	}

	pages = []scraper.Page{}
	for _, char := range characters {
		pages = append(pages, scraper.Page{Title: char.Name, Url: char.BaseUrl + char.Name})
	}

	pagesJson, err := json.MarshalIndent(pages, "", " ")
	if err != nil {
		log.Fatal(err)
	}

	err = os.WriteFile("character_pages.json", pagesJson, 0644)
	if err != nil {
		log.Fatal(err)
	}
}
