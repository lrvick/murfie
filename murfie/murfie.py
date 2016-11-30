# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
from http.cookiejar import LWPCookieJar
from urllib.request import HTTPCookieProcessor, build_opener
from urllib.parse import urlencode
from urllib.request import HTTPSHandler


class Murfie():

    def __init__(self):
        self.url = "https://www.murfie.com"
        self.cookies = LWPCookieJar()
        self.opener = build_opener(
            HTTPCookieProcessor(self.cookies),
            HTTPSHandler(debuglevel=0)
        )
        self.auth_token = self._get_auth_token()
        self.confdir = "%s/.murfie/" % os.environ['HOME']
        os.makedirs(self.confdir, exist_ok=True)

    def _get_auth_token(self, login=False):
        if login:
            url = "%s/users/login" % self.url
        else:
            url = "%s/account/password" % self.url
        html = self.opener.open(url).read()
        bs = BeautifulSoup(html, "lxml")
        auth_token = bs.select_one("input[name=authenticity_token]")["value"]
        if not auth_token:
            return Exception("Fetching auth token failed")
        return auth_token

    def login(self, email=None, password=None):
        self.auth_token = self._get_auth_token(login=True)
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
        self.auth_token = self._get_auth_token()
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
        success_url = \
            'https://www.murfie.com/deliveries/%s/download_requested' % disc_id
        url = "%s/deliveries/%s/create_download" % (self.url, disc_id)
        args = bytes(urlencode({
            "utf8": "✓",
            "authenticity_token": self.auth_token,
            "download_format_option": "2",
            "commit": "Request+Download",
        }), "utf-8")
        resp = self.opener.open(url, args)
        if resp.url != success_url:
            print(resp.url, success_url)
            raise Exception("Download request failed")
        return True
