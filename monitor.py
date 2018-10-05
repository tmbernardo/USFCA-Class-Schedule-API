from lxml import html
from random import randint
import os
import time
import re

def get_current():
    with open("fullsched.html", "r") as site: 
        count = 0
        url = "https://iris2.usfca.edu"
        tree = html.fromstring(str(site.read()))
        tree.make_links_absolute(url)

        titles = tree.xpath("//th[@class='ddtitle']/a/text()")
        names = tree.xpath("//table[@class='datadisplaytable']/tr[2]/td[7]/text()[1]")
        urls = tree.xpath("//th[@class='ddtitle']/a/@href")

        for title, name, url in zip(titles, names, urls):
            if count % 100 != 0:
                count += 1
                continue
            count += 1
            name = " ".join(re.sub("[\W+]", " ", name.lower()).split())
            name = re.sub("[\W+]", "-", name)
            pcourse = title.split('-')

            cap = randint(15,60)
            act = randint(0,cap)
            print()
            print("title:"+pcourse[0].split())
            print("crn:"+pcourse[1].strip())
            print("course_num:"+pcourse[2].split()[1].strip())
            print("section_num:"+pcourse[3].strip())
            print("capacity:"+str(cap))
            print("actual:"+str(act))
            print("course_url:"+url)
            print("instructor:"+name)
            print("dept:"+pcourse[2].split()[0].strip())



if  __name__ == "__main__":
    get_current()
