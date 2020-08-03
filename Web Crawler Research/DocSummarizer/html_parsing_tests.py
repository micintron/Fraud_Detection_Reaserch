from tkinter.filedialog import askopenfilename
from bs4 import BeautifulSoup
import tkinter as tk
import requests
import numpy as np
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from html.parser import HTMLParser
import nltk

#nltk.download('punkt')

def get_article(html: str):
    """
    Retrieves all text with the <p> html tag

    :param html: html page content retrieved from url
    :return: plaintext webpage contents
    """
    soup = BeautifulSoup(html, "html.parser")

    article_text = ''
    article = soup.find_all('p')
    for element in article:
        article_text += '\n' + ''.join(element.findAll(text=True))
    return article_text

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

'''

urls = ["https://www.broadstreethockey.com/2019/7/30/20706824/alain-vigneault-goalie-usage-history-flyers-nhl-carter-hart",
        "https://www.motorcyclenews.com/news/new-bikes/2019-triumph-rocket-3/",
        "https://www.nytimes.com/2019/07/30/us/california-gun-laws-gilroy.html"]

html_files = ["TestWebpages/Alain Vigneault’s career goalie usage history and how it impacts the Flyers - Broad Street Hockey.html",
              "TestWebpages/Triumph Rocket 3 unveiled.html",
              "TestWebpages/Guns Across Borders_ California Has Strict Laws, but Nevada Doesn’t - The New York Times.html"]


# Parse file using sumy.parsers.htmlparser
print("=================================================== SUMY HTMLPARSER ===========================================")
try:
    for i in range(len(html_files)):
        parser = HtmlParser.from_file(html_files[i], url="", tokenizer=Tokenizer('english'))
        print(html_files[i])
        print("-------------------------------------------------------------------------------------")
        webpage_content = ""
        for s in parser.document.sentences:
            webpage_content += str(s) + "\n"
        print(webpage_content.strip())
        print("-------------------------------------------------------------------------------------\n\n\n")
except:
    print("There was an error")


# Parse url using sumy.parsers.htmlparser
for i in range(len(urls)):
    parser = HtmlParser.from_url(urls[i], tokenizer=Tokenizer('english'))
    print(urls[i])
    print("-------------------------------------------------------------------------------------")
    webpage_content = ""
    for s in parser.document.sentences:
        webpage_content += str(s) + "\n"
    print(webpage_content.strip())
    print("-------------------------------------------------------------------------------------\n\n\n")

print("===============================================================================================================")
print("\n\n\n")

print("=================================================== BEAUTIFULSOUP =============================================")
# Parse file using beautifulsoup
try:
    for i in range(len(html_files)):
        print(html_files[i])
        print("-------------------------------------------------------------------------------------")
        html = open(html_files[i], "r").read()
        webpage_content = get_article(html)
        print(webpage_content.strip())
        print("-------------------------------------------------------------------------------------\n\n\n")
except:
    print("There was an error")

# Parse url using beautifulsoup
for i in range(len(urls)):
    print(urls[i])
    print("-------------------------------------------------------------------------------------")
    html = requests.get(urls[i]).content
    webpage_content = get_article(html)
    print(webpage_content.strip())
    print("-------------------------------------------------------------------------------------\n\n\n")

print("===============================================================================================================")
print("\n\n\n")
'''


# From a chosen file
root = tk.Tk().withdraw()  # removes tkinter default popup box
filepath = askopenfilename(filetypes=[("Webpage", ["*.html", "*.rtf"])])  # Only allow text files currently
parser = HtmlParser.from_file(filepath, url="", tokenizer=Tokenizer('english'))

def sumyParcer():
    print("------------------------- sumy parser --------------------------------------------")
    try:
        webpage_content = ""
        for s in parser.document.sentences:
            webpage_content += str(s) + "\n"
        print(webpage_content.strip())
    except:
        print("parcer failed - error  :")
    print("------------------------- end of sumy parser -------------------------------------\n\n\n")

def bs_Parcer():
    print("------------------------- beautiful soup --------------------------------------------")
    html = open(filepath, "r").read()
    webpage_content = get_article(html)
    print(webpage_content)
    print("------------------------- end of beautiful soup parser ------------------------------\n\n\n")

def htmlParcer():
    print("------------------------- html parcer --------------------------------------------")
    html = open(filepath, "r").read()
    parser = MyHTMLParser()
    webpage_content = parser.feed(html)
    print(webpage_content)
    print("------------------------- end of html parcer ------------------------------\n\n\n")

#sumyParcer()
#bs_Parcer()
htmlParcer()
