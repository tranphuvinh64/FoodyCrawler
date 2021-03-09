import scrapy
import os
import re
import pytz
from datetime import datetime

def getLinksFromFile(name):
    result = []
    with open(name,"r") as f:
        for line in f:
            line = line.strip()
            result.append(line)
    return result

class GetNumber(scrapy.Spider):
    name = 'num'
    # start_urls = getLinksToCrawl()
    start_urls = getLinksFromFile("FirstPageEachFilter.txt")

    def parse(self, response):
        link = response.url 
        xpath_number = "//div[@class= 'result-status-count']/div/span/text()"
        number = response.xpath(xpath_number).extract()
        with open("FirstPageEachFilter_crawled.txt","a+") as f:
            f.write(link)
            f.write("|")
            f.write(str(number))
            f.write("\n")