#!python

from __future__ import annotations
from typing import TYPE_CHECKING

from email.parser import BytesParser
from email.policy import default
from imaplib import IMAP4_SSL

from configparser import ConfigParser
from datetime import date, timedelta

from content_parser import parse_content

if TYPE_CHECKING:
    from configparser import SectionProxy


class IMAP4_SSL_EDITED(IMAP4_SSL):
    def enable(self, capability: str):
        typ, data = self._simple_command("ENABLE", capability)
        if typ == "OK" and "UTF8=ACCEPT" in capability.upper():
            self._mode_utf8()
        return typ, data


def get_config(fname) -> ConfigParser:
    config = ConfigParser()
    config.read(fname, encoding="utf8")
    return config


def get_id_pw(service: str) -> tuple[str, str]:
    account = get_config("account.ini")[service]
    return account["id"], account["pw"]


def get_search_criterion(section: SectionProxy) -> str:
    start_date = date.today() - timedelta(days=2)
    start_str = start_date.strftime("%d-%b-%Y")
    criteria = ["SINCE", start_str]
    criteria += ["FROM", section["address"], "SUBJECT", section["subject"]]
    return criteria


def main() -> None:
    config = get_config("config.ini")
    mail_parser = BytesParser(policy=default)
    with IMAP4_SSL_EDITED("imap.gmail.com", timeout=10) as imap:
        imap.login(*get_id_pw(config["service"]["name"]))
        imap.enable("UTF8=ACCEPT")

        imap.select(config["service"]["mailbox"], readonly=True)

        for section_name, section in config.items():
            if not section_name.startswith("from."):
                continue

            _, all_nums = imap.search(None, *get_search_criterion(section))
            print(all_nums)

            for num in all_nums[0].split():
                _, raw_data = imap.fetch(num, "(RFC822)")
                mail_data = mail_parser.parsebytes(raw_data[0][1])
                message_id = mail_data["Message-ID"]

                sender_name = section_name.split(".")[1]
                body = mail_data.get_body()
                print(parse_content(body.get_content(), sender_name))

        imap.close()


if __name__ == "__main__":
    main()
