from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

#class LinkParser inherits HTMLParser methods
class LinkParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for (key, value) in attrs: 
				if key == 'href':
					newUrl = parse.urljoin(self.baseURL, value)
					self.links = self.links + [newUrl]
	#get links from websites. 				
	def getLinks (self, url):
		self.links = []
		self.baseURL = url
		response = urlopen(url)
		#content type made to check only words
		if response.getheader('Content-Type') == 'text/html':
			htmlBytes = response.read()
			htmlString = htmlBytes.decode("utf-8")
			self.feed(htmlString)
			return htmlString, self.links
		else:
			return "",[]
	#spider that searches for the word in the webpage.  
	@staticmethod
	def spider(url, word, maxPages):
		pagesToVisit = [url]
		numberVisited = 0
		foundWord = False
		while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
			numberVisited = numberVisited +1
			url = pagesToVisit[0]
			pagesToVisit = pagesToVisit[1:]
			try:
				print(numberVisited, "Visiting: ", url)
				parser = LinkParser()
				data, links = parser.getLinks(url)
				if data.find(word) > -1:
					foundWord = True
				pagesToVisit = pagesToVisit + links
				print ("**SUCCESS!**")
			except:
				print ("**FAILED!**")

		if foundWord: 
			print ("The word", word, " was found at ", url)
		else:
			print("Sorry, Word not found")

a = LinkParser()
web = input('Enter the Website to search for the content: ')
word_search = input ('Enter the word to search :')
a.spider(web, word_search, 100)