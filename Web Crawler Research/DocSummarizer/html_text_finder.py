from bs4 import BeautifulSoup
import logging
import html2text
from urllib.request import urlopen

# Set up logging config
logging.basicConfig(filename='html_text_finder.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def print_menu():
    print("Please Select a Menu Option:")
    print("1. Enter Url to pull text using html2text")
    print("2. Enter URL to pull text with beautiful soup")
    print("3. Exit")


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


menu_choice = "0"

while menu_choice != "3":
    logging.debug("While Loop 1 started...")
    print()
    print_menu()
    menu_choice = input().strip()
    logging.debug("Menu Choice {} Selected...".format(menu_choice))

    if menu_choice == "1":      
        # Enter url to classify example http://news.bbc.co.uk/2/hi/health/2284783.stm
        url = input("Enter URL: ").strip()
        logging.debug("Entered URL: {}".format(url))
    
        html = urlopen(url).read()
        soup = BeautifulSoup(html)
        
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        
        # get text
        text = soup.get_text()
        print(html2text.html2text(text))

    elif menu_choice == "2":
        
        # Enter url to classify example http://news.bbc.co.uk/2/hi/health/2284783.stm
        url = input("Enter URL: ").strip()
        logging.debug("Entered URL: {}".format(url))
    
        html = urlopen(url).read()
        soup = BeautifulSoup(html)
        
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        
        # get text
        text = soup.get_text()       
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        print(text)
              
        logging.debug("url text found sucessfuly")

        
    else:
         print("Menu choice invalid to exit press 3:")

    logging.debug("End of While Loop 1 Reached")
