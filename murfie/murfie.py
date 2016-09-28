# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
from http.cookiejar import LWPCookieJar
from urllib.request import HTTPCookieProcessor, build_opener
from urllib.parse import urlencode


class Murfie():

    def __init__(self):
        self.url = "https://www.murfie.com"
        self.cookies = LWPCookieJar()
        self.opener = build_opener(HTTPCookieProcessor(self.cookies))
        self.auth_token = self._get_auth_token()
        self.opener.addheaders = [
            ('User-Agent', "Mozilla/5.0 (X11; Linux x86_64) \
                            AppleWebKit/537.36 (KHTML, like Gecko) \
                            Chrome/53.0.2785.116 Safari/537.36"),
            ('DNT', 1),
        ]
        self.confdir = "%s/.murfie/" % os.environ['HOME']
        os.makedirs(self.confdir, exist_ok=True)

    def _get_auth_token(self):
        html = self.opener.open("%s/users/login" % self.url).read()
        bs = BeautifulSoup(html, "lxml")
        auth_token = bs.select_one("input[name=authenticity_token]")["value"]
        if not auth_token:
            return Exception("Fetching auth token failed")
        return auth_token

    def login(self, email=None, password=None):
        if not email or not password:
            try:
                self.cookies.load(
                    '%s/cookies.txt' % self.confdir,
                    ignore_discard=True
                )
            except:
                return Exception("Login Failed")
        else:
            resp = self.opener.open(
                "%s/users/login" % self.url,
                bytes(urlencode({
                    "utf8": "✓",
                    "authenticity_token": self.auth_token,
                    "user[email]": email,
                    "user[password]": password,
                    "commit": "Sign in"
                }), "utf-8")
            )
            if resp.getcode() != 200:
                return Exception("Login Failed")
            self.cookies.save(
                '%s/cookies.txt' % self.confdir,
                ignore_discard=True
            )
        return True

    def _get_library_total_pages(self):
        html = self.opener.open("%s/library" % self.url).read()
        bs = BeautifulSoup(html, "lxml")
        num_pages = bs.select_one("span[class=last] a")["href"].split('=')[1]
        return int(num_pages)

    def get_library_disc_ids(self):
        page_num = 1
        total_pages = self._get_library_total_pages()
        disc_ids = []
        while page_num != total_pages:
            html = self.opener.open(
                "%s/library?page=%d" % (self.url, page_num)
            ).read()
            bs = BeautifulSoup(html, "lxml")
            for element in bs.select("div[class=deliver-link] a"):
                disc_id = element['href'].split('=')[1]
                disc_ids.append(disc_id)
            page_num += 1
        return disc_ids

    def request_disc_download(self, disc_id):
        resp = self.opener.open(
            "%s/deliveries/%s/create_download" % (self.url, disc_id),
            bytes(urlencode({
                "utf8": "✓",
                "authenticity_token": self.auth_token,
                "commit": "Request+Download"
            }), "utf-8")
        )
        if resp.getcode() != 200:
            return Exception("Download request failed")
        return True
