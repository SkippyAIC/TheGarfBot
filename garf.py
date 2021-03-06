"""
MIT License

Copyright (c) 2021 SkippyAIC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#syntax http://images.ucomics.com/comics/ga/{}/ga{}{}{}.gif

from urllib.request import urlopen
from urllib.error import HTTPError

class garf:
    
    def __init__(self, date: list):
        
        self.date = [] ## year, month, day
        self.url = "http://images.ucomics.com/comics/ga/{}/ga{}{}{}.gif" ## direct comic gif/jpg url
        self.monthsLmao = dict(enumerate(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], 1))
        
        if len(date) < 3 or len(date) > 3:
            raise Exception("InvalidDate")
    
        for number in date:
            if len(number) == 1:
                number = "0" + number
            self.date.append(number)
        self.fullDate = self.readableDate(self.date)
        
        url = self.url.format(date[0], date[0][2:], date[1], date[2])
        self.url = self.resolver(url)
        
    def readableDate(self, date):
        numberMonth = int(date[1])
        try:
            month = self.monthsLmao[numberMonth]
        except KeyError:
            raise Exception("InvalidDate")
        
        return "{} {}, {}".format(month, date[2], date[0])
    
    def resolver(self, url):
        for i in (".gif", ".jpg"):
            try:
                url = url.replace(".gif", i)
                page = urlopen(url).url
                return page
            except HTTPError:
                if ".jpg" in url:
                    raise Exception("InvalidDate")
                else:
                    continue
        
if __name__ == "__main__":
    from sys import argv
    argv = list(argv[1:])
    print(argv)
    garfield = garf(argv)
    print(garfield.url, garfield.date)
