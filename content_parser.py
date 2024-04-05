#!python

from __future__ import annotations
from typing import TYPE_CHECKING

import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import common

if TYPE_CHECKING:
    from typing import Literal


def parse_content(
    data: str,
    mail_date: datetime,
    sender: Literal[
        "linkedin",
        "saramin_ai",
        "saramin_today",
        "saramin_weekly",
        "saramin_scrap",
        "wanted",
        "blindhire",
    ],
) -> common.Jobs:
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
                record["date"] = "날짜 미상"
                record["company"], record["location"] = map(
                    lambda x: x.strip(), job.p.get_text().split(" · ")
                )
                record["origin"] = sender
                table.append(record)
        case "saramin_ai":
            jobs = soup.select("td td tr")
            jobs = jobs[1:11] + jobs[12:]

            table = []
            for job in jobs:
                record = {}
                record["url"] = job.a["href"].strip()
                record["name"] = job.strong.get_text().strip()
                record["date"] = job.p.span.get_text().strip()
                datelen = len(record["date"])
                try:
                    record["date"] = (
                        mail_date
                        + timedelta(days=int(re.search(r"\d+", record["date"]).group()))
                    ).strftime("~%Y-%m-%d")
                except (TypeError, ValueError, AttributeError):
                    pass
                record["company"] = job.p.get_text().strip()[:-datelen]
                record["location"] = "지역 미상"
                record["origin"] = sender
                table.append(record)
        case "saramin_today":
            jobs = soup.select("td td tr td div a:has(p)")

            table = []
            for job in jobs:
                record = {}
                record["url"] = job["href"].strip()
                record["name"] = job.span.select("p")[1].get_text()
                record["date"] = job.span.p.select("span")[1].get_text().strip()
                record["company"] = job.span.p.select("span")[0].get_text().strip()
                record["location"] = "지역 미상"
                record["origin"] = sender
                table.append(record)
        case "saramin_weekly":
            jobs = soup.select("td td td tr:has(a)")

            table = []
            for job in jobs:
                record = {}
                record["url"] = job.a["href"].strip()
                record["name"] = job.a.get_text().strip()
                record["date"] = job.select("div")[1].get_text().strip()
                try:
                    record["date"] = datetime.strptime(
                        record["date"][-5:], "%m/%d"
                    ).replace(year=mail_date.year)
                    if record["date"] < mail_date:
                        record["date"] = record["date"].replace(year=mail_date.year + 1)
                    record["date"] = record["date"].strftime("~%Y-%m-%d")
                except (TypeError, ValueError, IndexError):
                    pass
                record["company"] = job.p.get_text().strip()
                record["location"] = "지역 미상"
                record["origin"] = sender
                table.append(record)
        case "saramin_scrap":
            jobs = soup.select("td td tr:has(a)")
            jobs = jobs[1:-1]

            table = []
            for job in jobs:
                record = {}
                record["url"] = job.a["href"].strip()
                record["name"] = job.select("td")[1].get_text().strip()
                record["date"] = job.select("td")[2].get_text().strip()
                try:
                    if record["date"].startswith("D-"):
                        record["date"] = mail_date + int(record["date"][2:])
                    else:
                        record["date"] = datetime.strptime(
                            record["date"][:-3], "%m/%d"
                        ).replace(year=mail_date.year)
                        if record["date"] < mail_date:
                            record["date"] = record["date"].replace(
                                year=mail_date.year + 1
                            )
                    record["date"].strftime("~%Y-%m-%d")
                except (TypeError, ValueError, IndexError):
                    pass
                record["company"] = job.select("td")[0].get_text().strip()
                record["location"] = "지역 미상"
                record["origin"] = sender
                table.append(record)
        case "wanted":
            jobs = soup.select("td td td td td:has(pre)")
            jobs = jobs[::2]

            table = []
            for job in jobs:
                record = {}
                record["url"] = job.a["href"].strip()
                record["name"] = job.select("div")[2].get_text().strip()
                record["date"] = "날짜 미상"
                record["company"] = job.select("div")[1].get_text().strip()
                record["location"] = job.select("div")[4].get_text().strip()
                record["origin"] = sender
                table.append(record)
        case "blindhire":
            jobs = soup.select("td td td td td table:has(table)")

            table = []
            for job in jobs:
                record = {}
                record["url"] = job.a["href"].strip()
                record["name"] = job.select("div")[3].get_text().strip()
                record["date"] = "날짜 미상"
                record["company"] = job.select("div")[2].get_text().strip()
                record["location"] = "지역 미상"
                record["origin"] = sender
                table.append(record)

    return table
