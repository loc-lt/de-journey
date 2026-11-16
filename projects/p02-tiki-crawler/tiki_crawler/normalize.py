from __future__ import annotations

import html
import re
from html.parser import HTMLParser
from typing import Any


class DescriptionParser(HTMLParser):
    BLOCK_TAGS = {
        "address",
        "article",
        "aside",
        "blockquote",
        "br",
        "div",
        "dl",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "hr",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "section",
        "table",
        "tr",
        "ul",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.image_urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "img":
            src = attrs_dict.get("src")
            if src:
                self.image_urls.append(src.strip())
        if tag == "li":
            self.parts.append("\n- ")
        elif tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if data:
            self.parts.append(data)


def normalize_description(raw_html: str | None) -> tuple[str, list[str]]:
    if not raw_html:
        return "", []

    parser = DescriptionParser()
    parser.feed(raw_html)
    text = html.unescape("".join(parser.parts))
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    disclaimer_marker = "Giá sản phẩm trên Tiki đã bao gồm thuế theo luật hiện hành."
    if disclaimer_marker in text:
        text = text.split(disclaimer_marker, 1)[0].rstrip()

    image_urls: list[str] = []
    seen: set[str] = set()
    for url in parser.image_urls:
        if url and url not in seen:
            seen.add(url)
            image_urls.append(url)

    return text, image_urls


def extract_image_urls(product: dict[str, Any], description_image_urls: list[str]) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()

    for item in product.get("images") or []:
        if not isinstance(item, dict):
            continue
        for key in ("large_url", "base_url", "medium_url", "thumbnail_url", "small_url"):
            value = item.get(key)
            if value and value not in seen:
                seen.add(value)
                urls.append(value)

    for value in description_image_urls:
        if value and value not in seen:
            seen.add(value)
            urls.append(value)

    return urls


def transform_product(product: dict[str, Any]) -> dict[str, Any]:
    description, description_image_urls = normalize_description(product.get("description"))
    images = extract_image_urls(product, description_image_urls)
    return {
        "id": product.get("id"),
        "name": product.get("name"),
        "url_key": product.get("url_key"),
        "price": product.get("price"),
        "description": description,
        "images": images,
    }
