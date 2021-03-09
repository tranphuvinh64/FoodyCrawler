import scrapy
import os
import re
import pytz
from datetime import datetime

def getAllLinks():
    links = []
    if os.path.isfile("FoodyStoreLinks.txt"):
        with open("FoodyStoreLinks.txt","r") as f:
            for line in f:
                links.append(line.strip())
    return links

def getLinksFromFile(name):
    result = []
    with open(name,"r") as f:
        for line in f:
            line = line.strip()
            result.append(line)
    return result

def getCrawledLinks():
    links = []
    if os.path.isfile("CrawledData.txt"):
        with open("CrawledData.txt", "r") as f:
            for line in f:
                line = line.strip()
                link = line.split("|")[1]
                links.append(link)
    else:
        with open("CrawledData.txt", "a+") as f:
            pass
    return links

def getLinksToCrawl():
    result = list(set(getAllLinks()) - set(getCrawledLinks()))
    return result

if __name__ == '__main__':
    temp1 = set(getAllLinks())
    temp2 = set(getCrawledLinks())
    print(len(temp1))
    print(len(temp2))
    print(temp1 - temp2)

class Crawler(scrapy.Spider):
    name = 'all'
    # start_urls = getLinksToCrawl()
    start_urls = getLinksFromFile("huyen-cu-chi.txt")

    def parse(self, response):
        link = response.url 
        xpath_ten = "//div[@class='main-info-title']/h1/text()"
        xpath_duong = "//div[@class='res-common-add']//span/a/span[@itemprop ='streetAddress']/text()"
        xpath_quanhuyen = "//div[@class='res-common-add']//span/a/span[@itemprop ='addressLocality']/text()"
        xpath_infos = "//div[@class='new-detail-info-area']" # to get length
        ten = response.xpath(xpath_ten).extract_first()
        if ten is None:
            ten = "None"
        duong = response.xpath(xpath_duong).extract_first()
        if duong is None:
            duong = "None"
        quanhuyen = response.xpath(xpath_quanhuyen).extract_first()
        if quanhuyen is None:
            quanhuyen = "None"
        infos = response.xpath(xpath_infos)

        seperate = '|'
        thoigianhoatdong = "None"
        thoigianthichhop = "None"
        thoigianchuanbi = "None"
        nghile = "None"
        theloai = "None"
        succhua = "None"
        phongcach = "None"
        phuhop = "None"
        phucvucacmon = "None"
        dacdiem = "None"
        for i in range(1,len(infos) + 1):
            xpath_info_name = f"//div[@class='new-detail-info-area'][{i}]/div[1]/text()"
            info_name = response.xpath(xpath_info_name).extract_first()
            info_name = info_name.strip().lower()


            if info_name.find("hoạt động") != -1:
                xpath_info = f"//div[@class='new-detail-info-area'][{i}]/div[2]/span[2]/text()"
                thoigianhoatdong = response.xpath(xpath_info).extract_first()
                if isinstance(thoigianhoatdong, str):
                    thoigianhoatdong = thoigianhoatdong.strip()
                if thoigianhoatdong is None:
                    thoigianhoatdong = "None"


            if info_name.find("thích hợp") != -1:    
                xpath_info = f"//div[@class='new-detail-info-area'][{i}]/div[2]/a/text()"
                lst_thichhop = response.xpath(xpath_info).extract()
                if isinstance(lst_thichhop, list):
                    thoigianthichhop  = ""
                    for el in lst_thichhop:
                        thoigianthichhop = thoigianthichhop + str(el) + ','
                    thoigianthichhop = thoigianthichhop.strip()


            if info_name.find("chuẩn bị") != -1:
                xpath_info = f"//div[@class='new-detail-info-area'][{i}]/div[2]/span[1]/text()"
                thoigianchuanbi = response.xpath(xpath_info).extract_first()
                if isinstance(thoigianchuanbi, str):
                    thoigianchuanbi = thoigianchuanbi.strip()
                if thoigianchuanbi is None:
                    thoigianchuanbi = "None"
            
            if info_name.find("nghỉ lễ") != -1:
                xpath_info = f"//div[@class='new-detail-info-area'][{i}]/div[2]/span[1]/text()"
                nghile = response.xpath(xpath_info).extract_first()
                if isinstance(nghile, str):
                    nghile = nghile.strip()
                if nghile is None:
                    nghile = "None"
            
            if info_name.find("thể loại") != -1:
                xpath_info = f"//div[@class='new-detail-info-area'][{i}]/div[2]/a/text()"
                theloai = response.xpath(xpath_info).extract_first()
                if isinstance(theloai, str):
                    theloai = theloai.strip()
                if theloai is None:
                    theloai = "None"
            

            if info_name.find("sức chứa") != -1:
                xpath_info = f"//div[@class='new-detail-info-area'][{i}]/div[2]/span[1]/text()"
                succhua = response.xpath(xpath_info).extract_first()
                if isinstance(succhua, str):
                    succhua = succhua.strip()
                if succhua is None:
                    succhua = "None"

            if info_name.find("phong cách") != -1:
                xpath_info = f"//div[@class='new-detail-info-area'][{i}]/div[2]/a/text()"
                phongcach = response.xpath(xpath_info).extract_first()
                if isinstance(phongcach, str):
                    phongcach = phongcach.strip()
                if phongcach is None:
                    phongcach = "None"

            if info_name.find("phù hợp") != -1:
                xpath_info = f"//div[@class='new-detail-info-area'][{i}]/div[2]/a/text()"
                lst_phuhop = response.xpath(xpath_info).extract()
                if isinstance(lst_phuhop,list):
                    phuhop = ""
                    for el in lst_phuhop:
                        phuhop = phuhop + str(el) + ','
                    phuhop = phuhop.strip()

            if info_name.find("phục vụ") != -1:
                xpath_info = f"//div[@class='new-detail-info-area'][{i}]/div[2]/a/text()"
                lst_mon = response.xpath(xpath_info).extract()
                if isinstance(lst_mon,list):
                    phucvucacmon = ""
                    for el in lst_mon:
                        phucvucacmon = phucvucacmon + str(el) + ','
                    phucvucacmon = phucvucacmon.strip()

        xpath_dacdiem = "//ul[@class ='micro-property']/li[not(@class='none')]/a/text()"
        lst_dacdiem = response.xpath(xpath_dacdiem).extract()
        if isinstance(lst_dacdiem,list):
            dacdiem = ""
            for el in lst_dacdiem:
                dacdiem = dacdiem + str(el) + ',' 
            dacdiem = dacdiem.strip()

        now = datetime.now().strftime("%y-%m-%d %H-%M-%s")
        with open("CrawledData.txt","a+") as f:
            f.write(now)
            f.write(seperate)

            f.write(link.replace(seperate,"/"))
            f.write(seperate)

            f.write(ten.replace(seperate,"/"))
            f.write(seperate)

            f.write(duong.replace(seperate,"/"))
            f.write(seperate)

            f.write(quanhuyen.replace(seperate,"/"))
            f.write(seperate)

            f.write(thoigianhoatdong.replace(seperate,"/"))
            f.write(seperate)

            f.write(thoigianthichhop.replace(seperate,"/"))
            f.write(seperate)

            f.write(thoigianchuanbi.replace(seperate,"/"))
            f.write(seperate)

            f.write(nghile.replace(seperate,"/"))
            f.write(seperate)

            f.write(theloai.replace(seperate,"/"))
            f.write(seperate)

            f.write(succhua.replace(seperate,"/"))
            f.write(seperate)

            f.write(phongcach.replace(seperate,"/"))
            f.write(seperate)

            f.write(phuhop.replace(seperate,"/"))
            f.write(seperate)

            f.write(phucvucacmon.replace(seperate,"/"))
            f.write(seperate)
            
            f.write(dacdiem.replace(seperate,"/"))
            f.write("\n")