#!/usr/bin/env python3

import requests


	

q = input("enter a query: ")
sortBy = input ("sort by popularity or time?: ")


def parseQuery(q):

	result = []
	acc = ""
	for char in q:
		if char == ',':
			result.append(acc)
			acc = ""
		else:
			acc += char
	
	result.append(acc)
	
	return result



def requestQuery():

	queryVector = parseQuery(q)

	myString = ""
	
	for i in range(len(queryVector)):
		myString+= "q=" + queryVector[i] + "&" 

	return myString

print(requestQuery())
print("\n\n")

url = ("https://newsapi.org/v2/everything?" + 
	requestQuery() +  
	
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

length = response.get("totalResults")
articles = response.get("articles")

# an article has source(which is a dictionary with keys id and name), author, title, description, url, urlToImage, publishedAt, content(this is really big)




def printNice(aList): # with new lines added for clairty for large data sets

	i = 1
	for element in aList:
	
		print(i)
		print(element)
		print("\n")
		i+= 1


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


def tupleUp(articles): # this tuple returns the (title, date, url) triple we talked about
	
	result = []
		
	title = getInfo(articles, "title")
	date = getInfo(articles, "publishedAt")
	url = getInfo(articles, "url")

	for i in range(len(articles)):
		result.append((title[i], date[i], url[i]))

	return result


def generalTupleUp (articles):	# outputs the full 8-tuple

	result = []

	title = getInfo(articles, "title")
	date = getInfo(articles, "publishedAt")
	url = getInfo(articles, "url")
	
	source = getInfo(articles, "source")
	author = getInfo(articles, "author")
	description = getInfo(articles, "description")
	urlToImage = getInfo(articles, "urlToImage")
	content = getInfo(articles, "content")

	for i in range(len(articles)):
		result.append((title[i], date[i], url[i], source[i], author[i], description[i], urlToImage[i], content[i]))

	return result




printNice(tupleUp(articles))






