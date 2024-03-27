#!python

from __future__ import annotations
from typing import TYPE_CHECKING

from email.parser import BytesParser
from email.policy import default
from imaplib import IMAP4_SSL

from configparser import ConfigParser
from datetime import timedelta

import pickle

import common
from content_parser import parse_content
from page_maker import show_from_data

if TYPE_CHECKING:
    from typing import Any
    from configparser import SectionProxy


class IMAP4_SSL_EDITED(IMAP4_SSL):
    """
    IMAP4_SSL에서, `enable()`의 구현을 수정한 클래스.
    Gmail에서 `ENABLE`이 capabilities에 누락되었지만 실제로는 작동하기 때문.
    """

    def enable(self, capability: str) -> tuple[Any, Any]:
        """
        서버가 ENABLE Extension을 지원한다는 가정 하에,
        ENABLE 명령어를 송신한다.
        지원하는 건 imaplib과 마찬가지로 UTF8=ACCEPT 뿐이다.

        Args:
            capability (str): ENABLE 명령어의 인수.

        Returns:
            tuple[Any, Any]: IMAP4_SSL.enable()과 같음.
        """
        typ, data = self._simple_command("ENABLE", capability)
        if typ == "OK" and "UTF8=ACCEPT" in capability.upper():
            self._mode_utf8()
        return typ, data


def get_config(fname: str) -> ConfigParser:
    """
    파일명이 fname인 컨피그를 읽어온다.

    Args:
        fname (str): 컨피그 파일명(경로).

    Returns:
        ConfigParser: 해당 파일을 읽어들인 컨피그파서.
    """
    config = ConfigParser()
    config.read(fname, encoding="utf8")
    return config


def get_id_pw(service: str) -> tuple[str, str]:
    """
    메일 계정의 ID, PW를 가져온다.
    가져오는 파일은 `account.ini`임.

    Args:
        service (str): 메일 계정 서비스 이름.

    Returns:
        tuple[str, str]: id와 pw 튜플.
    """
    account = get_config("account.ini")[service]
    return account["id"], account["pw"]


def get_search_criterion(section: SectionProxy, days: int) -> list[str]:
    """
    IMAP SEARCH 명령어에 대하여,
    알맞은 CRITERION 인자를 반환한다.
    최근 N일 전까지의 특정 메일링 서비스의 메일로 보이는 메일을 가져올 수 있도록 인자를 생성한다.

    Args:
        section (SectionProxy): 컨피그 파일에 저장된 메일링 서비스의 섹션.
        days (int): 최근 며칠 전까지 가져올지.

    Returns:
        list[str]: CRITERION 인자에 사용할 수 있는 리스트. 언패킹해서 IMAP 객체의 SEARCH 명령에 넘겨줄 수 있다.
    """
    start_date = common.get_now() - timedelta(days=days)
    start_str = common.get_datestr(start_date)
    criteria = ["SINCE", start_str]
    criteria += ["FROM", section["address"], "SUBJECT", section["subject"]]
    return criteria


def remove_duplicated_records(table: common.Jobs) -> common.Jobs:
    keys = "url", "name", "date", "company", "location", "origin"
    temp = set()
    for record in table:
        temp.add(tuple(record.values()))
    return [dict(zip(keys, e)) for e in temp]


def main() -> None:
    """
    필요한 메일을 IMAP으로 모두 읽어와서,
    간단한 웹페이지(HTML) 형태로 보여준다.
    """
    config = get_config("config.ini")
    recent_days = int(config["config"]["recent_days"])
    mail_parser = BytesParser(policy=default)
    table = []

    try:
        with open(".already", "rb") as f:
            already = pickle.load(f)
    except FileNotFoundError:
        already = set()

    with IMAP4_SSL_EDITED("imap.gmail.com", timeout=10) as imap:
        imap.login(*get_id_pw(config["service"]["name"]))
        imap.enable("UTF8=ACCEPT")

        imap.select(config["service"]["mailbox"], readonly=True)

        for section_name, section in config.items():
            if not section_name.startswith("from."):
                continue

            _, all_nums = imap.search(None, *get_search_criterion(section, recent_days))

            for num in all_nums[0].split():
                _, raw_data = imap.fetch(num, "(RFC822)")
                mail_data = mail_parser.parsebytes(raw_data[0][1])
                message_id = mail_data["Message-ID"]

                if message_id in already:
                    continue

                already.add(message_id)
                sender_name = section_name.split(".")[1]
                body = mail_data.get_body()
                # with open("test.txt", "wt", encoding="utf8") as f:
                #     print(body.get_content(), file=f)
                # break
                table += parse_content(body.get_content(), sender_name)

        table = remove_duplicated_records(table)
        show_from_data(table)
        imap.close()


if __name__ == "__main__":
    main()
