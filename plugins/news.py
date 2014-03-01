import io
import requests
import unittest
import urllib.parse


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        topic = " ".join(msg["args"][1:])
        if not topic:
            topic = stdin.read().strip()

        if topic:
            url = "https://ajax.googleapis.com/ajax/services/search/news?v=1.0&rsz=5&q={0}".format(
                urllib.parse.quote(topic)
            )
        else:
            url = "https://ajax.googleapis.com/ajax/services/search/news?v=1.0&rsz=5&topic=h"

        headers = {"User-Agent": "SmartBot"}

        res = requests.get(url, headers=headers).json()
        stories = res["responseData"]["results"][:3]
        if stories:
            for i, story in enumerate(stories):
                title = story["titleNoFormatting"].replace("&#39;", "'").replace("`", "'").replace("&quot;", "\"")
                link = story["unescapedUrl"]
                print("[{0}]: {1} - {2}".format(i, title, link), file=stdout)
        else:
            print("No news stories.", file=stdout)

    def on_help(self):
        return "Syntax: news [<topic>]"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

    def test_no_category(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertNotEqual("No news stories.", stdout.getvalue().strip())

    def test_category(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None, "cats"]}, stdout, stdout, None)
        self.assertNotEqual("No news stories.", stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())
