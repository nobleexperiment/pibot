from html.parser import HTMLParser
from urlib.request import urlopen
from urlib import parse

class LinkParser (HTMLParser):

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for (key, value) in attrs:
				if key == 'href':
					newUrl = parse.urljoin(self.baseUrl, value)
					self.links = self.links + [newUrl]

	def getLinks(self, url):
		self.links = []
		self.baseUrl = url
		response = urlOpen(url)
		if response.getheader('Content-Type')=='text/html':
			htmlBytes = response.read()
			htmlString = htmlBytes.decode("utf-8")
			self.feed(htmlstring)
			return htmlString, self.links
		else:
			return "",[]

def spider(url, word, maxPages):
	pagesToVisit = [url]
	numberVisited = 0
	foundWord = False
	while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
		numberVisited = numberVisited +1
		url = pagesToVisit[0]
		pagesToVisit = pagesToVisit[1:]
		try:
			print(numberVisited, "Visiting:", url)
			parser = LinkParser()
			data, links = parser.getLinks(url)
			if data.find(word)>-1:
				foundWord = True
			pagesToVisit = pagesToVisit + links
			print(" **Yup!**")
		except:
			print(" **Nope!**")
	if foundWord:
		print("The word", word, "was found at", url)
	else:
		print("Word never found")
