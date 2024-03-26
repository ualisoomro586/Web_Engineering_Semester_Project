from django.http.response import HttpResponse
from django.shortcuts import render
import requests
import bs4


# Create your views here.
def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def search(request):
    word = request.GET["word"]

    res = requests.get("https://www.dictionary.com/browse/" + word)
    res2 = requests.get("https://www.thesaurus.com/browse/" + word)

    if res:
        soup = bs4.BeautifulSoup(res.text, "lxml")

        meaning = soup.find_all("p", {"class": ""})
        # meaning = soup.find_all('div', {'value': '1'})
        meaning1 = meaning[0].getText()
    else:
        word = "Sorry, " + word + " Is Not Found In Our Database"
        meaning = ""
        meaning1 = ""

    if res2:
        soup2 = bs4.BeautifulSoup(res2.text, "lxml")

        synonyms = soup2.find_all("a", {"class": "KmScG4NplKj_3H5E3oA_"})

        # synonyms = soup2.find_all("a", {"class": "css-1kg1yv8 eh475bn0"})
        ss = []
        for b in synonyms[0:]:
            re = b.text.strip()
            ss.append(re)
        se = set(ss)

        antonyms = soup2.find_all(
            "a",
            {
                "class": "SynonymAndAntonymCard-module_s50_ce9743e40a27913a0580 SynonymAndAntonymCard-module_antonym_d70dabe8d34f0b3020a3"
            },
        )
        # antonyms = soup2.find_all("a", {"class": "css-15bafsg eh475bn0"})
        aa = []
        for c in antonyms[0:]:
            r = c.text.strip()
            aa.append(r)
        ae = set(aa)
    else:
        se = ""
        ae = ""

    results = {
        "word": word,
        "meaning": meaning1,
    }

    return render(request, "search.html", {"se": se, "ae": ae, "results": results})
