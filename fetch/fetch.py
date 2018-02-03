import urllib.request
import re
from bs4 import BeautifulSoup
import string


# URL Templates
poemURLTemplate = "http://uppagus.com/poems/"
flashFictionTemplate = "http://uppagus.com/flash-fiction/"

def getHTML(url):
	page = urllib.request.urlopen(url).read()
	
	soup = BeautifulSoup(page, 'lxml')
	return soup

def parseFileTree(soup):
	a = soup.findAll("a")
	regex = re.findall(r'<a href="(.*?)">', str(a))
	del regex[:5] # get rid of gibberish links at the beginning
	return regex

def parsePage(url, format):
	newUrl = "http://uppagus.com/" + format + "/" + url
	newsoup = getHTML(newUrl)

	p = newsoup.findAll("p")
	pString = ""
	for node in p:
		pString += str(node.findAll(text=True)) 
	pString = pString.replace("[","").replace("]","").replace("\\n","").replace("\\xa0","") # there will be a bunch of extra commas and spaces, but that shouldn't matter
	return pString


# get poems text
poemSoup = getHTML(poemURLTemplate)
poems = parseFileTree(poemSoup)

poemsText = ""
for x in poems:
	text = parsePage(x, 'poems')
	poemsText += " " + text


# get flash fiction text
fictionSoup = getHTML(flashFictionTemplate)
fiction = parseFileTree(fictionSoup)

fictionText = ""
for x in fiction:
	text = parsePage(x, 'flash-fiction')
	fictionText += " " + text

# write poems text to file
poemsFile = open("poems.txt", "wb")
poemsFile.write(poemsText.encode('ascii', 'ignore'))
poemsFile.close()

# write flash fiction text to file
fictionFile = open("fiction.txt", "wb")
fictionFile.write(fictionText.encode('ascii', 'ignore'))
fictionFile.close()

# write both poems and flash fiction text to same file
combinedFile = open("combined.txt", "wb")
poemsText += " "
combinedFile.write(poemsText.encode('ascii', 'ignore') + fictionText.encode('ascii', 'ignore'))
combinedFile.close()
