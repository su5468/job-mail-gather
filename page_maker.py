#!python

from __future__ import annotations
from typing import TYPE_CHECKING

import webbrowser

from bs4 import BeautifulSoup

import common

if TYPE_CHECKING:
    from bs4 import Tag


def make_page(content: common.Jobs) -> str:
    soup = BeautifulSoup("<!DOCTYPE html>", features="html.parser")
    html = make_tag_inside_of(soup, soup, "html", attrs={"lang": "ko"})

    head = make_head(html, soup)
    body = make_body(html, soup, content)

    return soup.prettify()


def make_head(html: Tag, soup: BeautifulSoup) -> Tag:
    head = make_tag_inside_of(html, soup, "head")
    make_tag_inside_of(head, soup, "meta", attrs={"charset": "utf-8"})
    make_tag_inside_of(
        head,
        soup,
        "meta",
        attrs={"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
    )
    make_tag_inside_of(
        head,
        soup,
        "meta",
        attrs={"http-equiv": "X-UA-Compatible", "content": "IE=edge,chrome=1"},
    )
    make_tag_inside_of(
        head, soup, "link", attrs={"rel": "stylesheet", "href": "styles.css"}
    )
    title = make_tag_inside_of(head, soup, "title")
    title.string = "Job Mail Gather"

    return head


def make_body(html: Tag, soup: BeautifulSoup, content: common.Jobs) -> Tag:
    body = make_tag_inside_of(html, soup, "body")
    header = make_tag_inside_of(body, soup, "header")
    h1 = make_tag_inside_of(header, soup, "h1")
    h1.string = "Job Mail 리스트"
    h2 = make_tag_inside_of(header, soup, "h2")
    hr = make_tag_inside_of(body, soup, "hr")

    article = make_tag_inside_of(body, soup, "article")

    h2.string = f"기준일: {common.get_now()}"
    for record in content:
        ul = make_tag_inside_of(article, soup, "ul")
        div_job = make_tag_inside_of(
            ul,
            soup,
            "div",
            attrs={
                "class": "div-job",
                "onclick": f"window.open('{record['url']}', '_blank')",
            },
        )
        h2 = make_tag_inside_of(div_job, soup, "h2")
        span_companyName = make_tag_inside_of(
            h2, soup, "span", attrs={"class": "span-companyName"}
        )
        span_jobType = make_tag_inside_of(
            h2, soup, "span", attrs={"class": "span-jobType"}
        )
        div_jobLocation = make_tag_inside_of(
            div_job, soup, "div", attrs={"class": "div-jobLocation"}
        )
        div_date = make_tag_inside_of(div_job, soup, "div", attrs={"class": "div-date"})
        div_origin = make_tag_inside_of(
            div_job, soup, "div", attrs={"class": "div-origin"}
        )

        span_companyName.string = record["company"]
        span_jobType.string = record["name"]
        div_jobLocation.string = record["location"]
        div_date.string = record["date"]
        div_origin.string = record["origin"]

    return body


def make_tag_inside_of(parent: Tag, soup: BeautifulSoup, *args, **kwargs) -> Tag:
    tag = soup.new_tag(*args, **kwargs)
    parent.append(tag)
    return tag


def save_page(page: str, fname: str = "page.html") -> None:
    with open(fname, "wt", encoding="utf8") as f:
        f.write(page)
    return fname


def show_page(url: str) -> None:
    webbrowser.open(url)


def show_from_data(data: common.Jobs) -> None:
    page = make_page(data)
    datestr = common.get_datestr(common.get_now())
    url = save_page(page, f"jobs-{datestr}.html")
    show_page(url)


def main() -> None:
    show_from_data([{"테스트", "테테"}, {"소스트", "소소"}])


if __name__ == "__main__":
    main()
