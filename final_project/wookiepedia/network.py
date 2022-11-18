import xml.etree.ElementTree as ET
import requests

def get_pages(url: str) -> dict:
    site_map_str = "/sitemap-newsitemapxml-index.xml"
    response = requests.get(url + site_map_str, timeout=5)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    elements = {}
    for page in root.iter(namespace + "loc"):
        response = requests.get(page.text, timeout=5)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        for element in root.iter(namespace + "loc"):
            elements[element.text.split("/")[-1]] = element.text

    return elements
