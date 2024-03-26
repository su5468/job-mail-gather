#!python

from __future__ import annotations
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from typing import Literal, Any


def parse_content(data: str, sender: Literal["linkedin"]) -> list[dict[str, Any]]:
    """
    주어진 메일 본문 문자열을 파싱한다.

    Args:
        data (str): 메일 본문 문자열.
        sender (Literal["linkedin"]): 메일링 서비스 이름.

    Returns:
        list[dict[str, Any]]: 구인 공고(딕셔너리)들의 리스트.
    """
    soup = BeautifulSoup(data, "html.parser")
    match sender:
        case "linkedin":
            jobs = soup.select(
                'table[role="presentation"] ' * 5
                + 'a[target="_blank"] > '
                + 'table[role="presentation"]'
            )

            table = []
            for job in jobs:
                record = {}
                record["url"] = job.a["href"].strip()
                record["name"] = job.a.get_text().strip()
                record["company"], record["location"] = map(
                    lambda x: x.strip(), job.p.get_text().split(" · ")
                )
                table.append(record)

            return table
