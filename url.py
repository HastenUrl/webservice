from typing import Dict
import string

ELEMENTS = string.digits + string.ascii_letters

class UrlService:
  base_url: str
  elements: str
  counter = 10000
  ltos: Dict[int, str] = {}
  stol: Dict[str, int] = {}

  def __init__(self, base: str):
    self.elements = ELEMENTS
    self.base_url = base

  def generate(self):
    shorturl = self.base10tobase62(self.counter)
    self.ltos[shorturl] = self.counter
    self.stol[self.counter] = shorturl
    self.counter += 1
    return self.base_url + shorturl

  def shortToLong(self, base: str, url: str):
    short_url = url[len(base): len(url)]
    return self.base62tobase10(short_url)

  def base10tobase62(self, n: int):
    sb = ""
    while (n != 0):
      r = int(n % 62)
      sb = self.elements[r] + sb
      n = int((n - r) / 62)
    return sb

  def base62tobase10(self, url: str):
    n = 0
    for i in range(len(url)):
        n = (n * 62) + (self.elements.index(url[i]))
    return n

base_url = "https://a.com/"
us = UrlService(base_url)
for i in range(100):
  new_url = us.generate()
  print(new_url, us.shortToLong(base_url, new_url))
