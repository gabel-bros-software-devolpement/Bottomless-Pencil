from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import gensim
from gensim.models import Word2Vec

num = "000"

speeches = []
speechWords = [[]]

for i in range(0, 50):
    num = str("{:03d}".format(i))
    f = open("C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\speeches\\obama_speeches_" + num + ".txt", "r")
    speeches.append(f.read())
    tokens = word_tokenize(speeches[i])
    stop_words = set(stopwords.words("english"))
    tokens = [w for w in tokens if not w in stop_words]
    porter = PorterStemmer()
    speechWords.append([])
    for t in tokens:
        speechWords[i].append(porter.stem(t).lower())

speeches.remove(speeches[24])
speeches.remove(speeches[25])
speechWords.remove(speechWords[24])
speechWords.remove(speechWords[25])

for i in range(0, 39):
    num = str("{:03d}".format(i))
    f = open("C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\speeches\\clinton_speeches_" + num + ".txt", "r")
    speeches.append(f.read())
    tokens = word_tokenize(speeches[i+46])
    stop_words = set(stopwords.words("english"))
    tokens = [w for w in tokens if not w in stop_words]
    porter = PorterStemmer()
    speechWords.append([])
    for t in tokens:
        speechWords[i+46].append(porter.stem(t).lower())



site = "https://www.isidewith.com/elections/2020-presidential-quiz"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
webSite = BeautifulSoup(page,"html.parser")

questions = []
questionsBasic = [[]]
try:
    for x in range(0,pow(10,10)):
        speeches.append(webSite.findAll("h3")[x].get_text().replace("?",""))
        tokens = word_tokenize(speeches[len(speeches)-1])
        stop_words = set(stopwords.words("english"))
        tokens = [w for w in tokens if not w in stop_words]
        porter = PorterStemmer()
        speechWords.append([])
        for t in tokens:
            speechWords[len(speeches)-1].append(porter.stem(t))
except:
    print("Retrieved all questions.txt\n\n")

# ###############################################
# for i in range(1, 37):
#     num = str("{:03d}".format(i))
#     f = open("C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\speeches\\clintonH_" + num + ".txt", "r")
#     speeches.append(f.read())
#     tokens = word_tokenize(speeches[len(speeches)-1])
#     stop_words = set(stopwords.words("english"))
#     tokens = [w for w in tokens if not w in stop_words]
#     porter = PorterStemmer()
#     speechWords.append([])
#     for t in tokens:
#         speechWords[len(speeches)-1].append(porter.stem(t).lower())
#
# for i in range(1, 81):
#     num = str("{:03d}".format(i))
#     f = open("C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\speeches\\Trump_" + num + ".txt", "r")
#     speeches.append(f.read())
#     tokens = word_tokenize(speeches[len(speeches)-1])
#     stop_words = set(stopwords.words("english"))
#     tokens = [w for w in tokens if not w in stop_words]
#     porter = PorterStemmer()
#     speechWords.append([])
#     for t in tokens:
#         speechWords[len(speeches)-1].append(porter.stem(t).lower())
# ##################################################

sWords = ["'", ".", "<", ">", "(", ")", "-", ",", "/", ":", ";", "\"", "!", "?", "'s", "i", "we", "the", "and", "--", "it", "should"]
for y in speechWords:
    for x in y:
        for w in sWords:
            if (x == w):
                y.remove(x)
                break

for i in range(0, len(speeches)):
    print("speech " + str(i) + ":\t" + str(speechWords[i]))

model1 = gensim.models.Word2Vec(speechWords, min_count=1, size=10, window=5)

model1.save("word2vecPolitical.model")

for x in range(10):
    w = porter.stem(input("Enter a word to test: "))
    print(w+": "+str(model1.most_similar(positive=w)))
