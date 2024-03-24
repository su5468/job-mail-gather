#!python

from __future__ import annotations
from typing import TYPE_CHECKING

from html.parser import HTMLParser

if TYPE_CHECKING:
    from typing import Literal


class HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.data = []
        self.not_to_parse = {"script", "style"}
        self.appending = False

    def handle_starttag(self, tag, _):
        if tag in self.not_to_parse:
            self.appending = False
        else:
            self.appending = True

    def handle_data(self, data: str) -> None:
        if self.appending:
            self.data.append(data)

    def get_data_str(self) -> str:
        return " ".join(self.data)


def parse_content(data: str, sender: Literal["linkedin"]) -> str:
    match sender:
        case "linkedin":
            text_extractor = HTMLTextExtractor()
            text_extractor.feed(data)
            return text_extractor.get_data_str()
