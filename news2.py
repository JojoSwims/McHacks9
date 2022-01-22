#!/usr/bin/env python3

import requests




q = input("enter a query: ")
sortBy = input ("popularity or time?: ")


url = ("https://newsapi.org/v2/everything?" + 
	"q="+q + "&" +  
	
	"sortBy=" + sortBy + "&"

	"apiKey=06fa07b7b84a486699e92bc6af7a9c45"
		
	)


# url2 is a model for url
url2 = ('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'from=2022-01-22&'
       'sortBy=popularity&'
	'apiKey=06fa07b7b84a486699e92bc6af7a9c45')


response = requests.get(url).json()


articles = response.get("articles")

# an article has source(which is a dictionary with keys id and name), author, title, description, url, urlToImage, publishedAt, content(this is really big)




def printNice(aList): # with new lines added for clairty for large data sets
	for element in aList:
		print(element)


def parseTime (date):
	date = date.rstrip(date[-1])		#remove the Z at the end
	result = []
	acc = ""
	for char in date:
		if char == '-' or char == 'T' or char == ':':
			result.append(acc)
			acc = ""
		else:
			acc += char
			
	return result	


def getInfo (articles, attribute): 	# attribute is a string like "author", "title", or "url"
	attributes = []
		
	validAttributes = ["source", "author", "title", "description", "url", "urlToImage", "publishedAt", "content"]
	
	if not (attribute in validAttributes):
		return []

	for article in articles:

		
		if attribute == "source":
			attributes.append(article.get("source").get("name"))		# we assume name of the source is more relevant than id of the source
		else:
			attributes.append(article.get(attribute))
		
	
	return attributes


def getRank(articles, rankBy, objOfInterest):

	info = getInfo(articles, rankBy)
	
	i = 1			# the ith rank
	n = len(info)
	for element in info:
		if element == objOfInterest:
			return i
		i += 1
		
	if i > n:
		return -1 		# object was not in the list





printNice (getInfo(articles, "source"))


print(getRank(articles, "title", " Kazakhstan Descends into Chaos, Crypto Miners Are at a Loss"))



