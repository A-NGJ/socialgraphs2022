package scraper

type Page struct {
	Title string
	Url   string
}

type Character struct {
	Name       string    `json:"name"`
	SideBars   []SideBar `json:"side_bars"`
	Content    string    `json:"content"`
	BaseUrl    string    `json:"base_url"`
	Crosslinks []string  `json:"crosslinks"`
}

type SideBar struct {
	Name       string      `json:"name"`
	Attributes []Attribute `json:"attributes"`
}

type Attribute struct {
	Name   string   `json:"name"`
	Values []string `json:"values"`
}