package scraper

import (
	"strings"

	"github.com/A-NGJ/socialgraphs2022/utils"
	"github.com/gocolly/colly"
)

func Scrape(pages []Page) ([]Character, error) {
	var characters []Character

	collector := colly.NewCollector(
		colly.AllowedDomains("starwars.fandom.com"),
		colly.Async(true),
	)

	collector.Limit(&colly.LimitRule{DomainGlob: "*", Parallelism: 50})

	collector.OnHTML("main.page__main", func(elem *colly.HTMLElement) {
		var isCharacter bool
		var character Character = Character{BaseUrl: "https://starwars.fandom.com/"}

		character.Name = elem.ChildText("h1#firstHeading")

		elem.ForEach("section.pi-item", func(_ int, el *colly.HTMLElement) {
			var sideBar SideBar = SideBar{}
			var attr Attribute = Attribute{}

			sideBar.Name = el.ChildText("h2")
			el.ForEach("div.pi-item", func(_ int, el1 *colly.HTMLElement) {
				attr.Name = el1.ChildText("h3.pi-data-label")
				var attributes []string
				var rawAttributes []string

				if attr.Name == "Species" {
					isCharacter = true
				}
				attributesListText := el1.ChildText("ul")
				if attributesListText != "" {

					el1.ForEach("li", func(_ int, el2 *colly.HTMLElement) {

						rawAttributes = strings.Split(
							utils.SetDelimiter(
								utils.RemoveSupText(el2.Text, ","),
								","),
							",")
						rawAttributes = utils.RemoveFromSlice(rawAttributes, "")
						for i, attr := range rawAttributes {
							rawAttributes[i] = strings.TrimSpace(attr)
						}
						attributes = append(attributes, rawAttributes...)
					})
				} else {
					rawAttributes = strings.Split(utils.RemoveSupText(el1.ChildText("div"), ""), ",")
					rawAttributes = utils.RemoveFromSlice(rawAttributes, "")
					for i, attr := range rawAttributes {
						rawAttributes[i] = strings.TrimSpace(attr)
					}
					attributes = append(attributes, rawAttributes...)
				}
				attr.Values = attributes
				sideBar.Attributes = append(sideBar.Attributes, attr)
			})
			character.SideBars = append(character.SideBars, sideBar)
		})
		if isCharacter {
			var content string
			var crosslinks []string

			// if page describes character, scan for its content
			content = elem.ChildText("div.mw-parser-output > p")
			content = utils.RemoveSupText(content, "")
			// err := os.WriteFile("data/contents/"+character.Name+".txt", []byte(content), 0644)
			// if err != nil {
			// 	log.Printf("ERROR: error while writing { %s } content: %s\n", character.Name, err)
			// }
			character.Content = content

			crosslinks = elem.ChildAttrs("div.mw-parser-output a[href]", "href")
			crosslinks = utils.RemoveFromSliceRegex(crosslinks, "wiki", true)
			crosslinks = utils.RemoveFromSliceRegex(crosslinks, "http(s)?", false)
			character.Crosslinks = utils.RemoveDuplicates(crosslinks)

			// finally append the character with all the data
			characters = append(characters, character)
		}
	})

	// visit and scrape pages using defined above callbacks
	for _, page := range pages {
		// fmt.Printf("\rPage %d out of %d", i, len(pages))
		collector.Visit(page.Url)
	}
	collector.Wait()

	return characters, nil
}
