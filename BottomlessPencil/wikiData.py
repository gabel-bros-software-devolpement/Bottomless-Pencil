from pprint import pprint
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def getData(sch):
    x = sch.replace(" ","+")
    site = f"https://en.wikipedia.org/w/index.php?search={x}&title=Special%3ASearch&go=Go&ns0=1"
    hdr = {'User-Agent': 'erjnvbsflbn'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    webSite = BeautifulSoup(page,"html.parser")
    print(site)
    colors = []
    students = ""
    staff = ""
    for x in webSite.findAll("span"):
        if("background-color" in str(x)):
            #print(str(x)[str(x).index("#"):str(x).index("#")+7])
            colors.append(str(x)[str(x).index("#"):str(x).index("#")+7])
    for x in webSite.findAll():
        if(x.get_text()=="Academic staff"):
            #print(webSite.findAll()[webSite.findAll().index(x)+1].get_text())
            staff = webSite.findAll()[webSite.findAll().index(x)+1].get_text()
        if(x.get_text()=="Students"):
            #print(webSite.findAll()[webSite.findAll().index(x)+1].get_text())
            students = webSite.findAll()[webSite.findAll().index(x)+1].get_text()

    return {
        "colors":colors,
        "students":students,
        "staff":staff
    }

print(getData("virgina tech"))