from flask import Flask, render_template, url_for
from formsBP import takeInput
from flask import flash
from flask import redirect
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

app = Flask(__name__)

app.config['SECRET_KEY'] = '8c97ffcd72439fe7362f78a1f64c8423'

def cleanNum(dat):
    temp = ""
    if("(" in dat):
        temp=dat[:dat.index("(")]
    elif("[" in dat):
        temp=dat[:dat.index("[")]
    else:
        return dat
    return temp

def cleanSpace(dat):
    if(" " in dat):
        return dat[:dat.index(" ")]
    return dat

def cleanCamp(dat):
    dat=dat.strip()
    temp = ""
    if(":" in dat and "a" in dat):
        temp = dat[dat.index(":")+1:]
        temp=temp[:dat.index("a")+2]
    elif("," in dat and "a" in dat):
        temp = dat[dat.index(",")+1:]
        temp=temp[:dat.index("a")+1]
    else:
        temp=dat#dat[:dat.index("a")]
    if("a" in temp):
        temp = temp[:temp.index('a')]
    if("u" in temp.lower()):
        temp=""
    return temp

def removeDash(dat):
    if('-' in dat):
        return dat[:dat.index('-')]
    return dat

def getData(sch):
    x = str(sch).replace(" ","+")
    site = f"https://en.wikipedia.org/w/index.php?search={x}&title=Special%3ASearch&go=Go&ns0=1"
    hdr = {'User-Agent': ''}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    webSite = BeautifulSoup(page,"html.parser")
    #print(site)
    colors = []
    students = ""
    staff = ""
    web = ""
    typ = ""
    camp = ""
    loc = ""
    prez = ""
    for x in webSite.findAll("span"):
        if("background-color" in str(x)):
            #print(str(x)[str(x).index("#"):str(x).index("#")+7])
            colors.append(str(x)[str(x).index("#"):str(x).index("#")+7])
    for x in webSite.findAll():
        if(x.get_text()=="Academic staff"):
            #print(webSite.findAll()[webSite.findAll().index(x)+1].get_text())
            staff = webSite.findAll()[webSite.findAll().index(x)+1].get_text()
        if(x.get_text()=="Students" and "th" in str(x)):
            #print(webSite.findAll()[webSite.findAll().index(x)+1].get_text())
            students = webSite.findAll()[webSite.findAll().index(x)+1].get_text()
        if(x.get_text()=="Website"):
            #print(webSite.findAll()[webSite.findAll().index(x)+1].get_text())
            web = "http://"+webSite.findAll()[webSite.findAll().index(x)+1].get_text()
        if(x.get_text()=="Type"):
            #print(webSite.findAll()[webSite.findAll().index(x)+1].get_text())
            typ = webSite.findAll()[webSite.findAll().index(x)+1].get_text()
        if(x.get_text()=="Campus"):
            if("acres" in webSite.findAll()[webSite.findAll().index(x)+1].get_text()):
                camp = webSite.findAll()[webSite.findAll().index(x)+1].get_text()
        if(x.get_text()=="Location"):
            loc = webSite.findAll()[webSite.findAll().index(x)+1].get_text()
            loc=loc[:loc.index("U")-2]
        if(x.get_text()=="President"):
            #print(webSite.findAll()[webSite.findAll().index(x)+1].get_text())
            prez = webSite.findAll()[webSite.findAll().index(x)+1].get_text()
        
    return {
        "name":sch,
        "colors":colors,
        "students":cleanNum(students),
        "staff":cleanNum(staff),
        "type":removeDash(cleanNum(cleanSpace(typ))),
        "camp":cleanCamp(camp),
        "loc":loc.split(","),
        "prez":cleanNum(prez),
        "url":web
    }

schools = []

@app.route('/', methods=['GET', 'POST']) 
def home():
    form = takeInput()
    try:
        schools.append(getData(form.school.data))
    except:
        print('School not found')
    for x in schools:
        if(len(x['colors'])<1):
            schools.remove(x)
    return render_template("home.html",title='Bottomless Pencil',form=form,schools=schools)

if __name__ == "__main__":
    app.run(debug=True)

