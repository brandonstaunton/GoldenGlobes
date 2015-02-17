# -*- coding: iso-8859-15 -*-
from Tkinter import *
import unicodedata
import pprint
import Winners

# Award types
MOTION_PICTURE = 1
TELEVISION = 2
DRAMA = 4
COMEDY = 8
ACTOR = 16
ACTRESS = 32
SUPPORTING = 64
SONG = 128
SCORE = 256
ANIMATED = 512
FOREIGN = 1024

# Array that holds which awards contain the above words
classificationWords = []

def transpose(matrix):
	height = len(matrix)
	width = len(matrix[0])
	return [[ matrix[row][col] for row in range(0,height) ] for col in range(0,width) ]

def buildClassifications():
	global classificationWords
	classificationWords = [0] * len(categories)
	for c, category in enumerate(categories):
		if "motion" in category.lower(): classificationWords[c] |= MOTION_PICTURE
		if "television" in category.lower(): classificationWords[c] |= TELEVISION
		if "drama" in category.lower(): classificationWords[c] |= DRAMA
		if "comedy" in category.lower(): classificationWords[c] |= COMEDY
		if "actor" in category.lower(): classificationWords[c] |= ACTOR
		if "actress" in category.lower(): classificationWords[c] |= ACTRESS
		if "supporting" in category.lower(): classificationWords[c] |= SUPPORTING
		if "song" in category.lower(): classificationWords[c] |= SONG
		if "score" in category.lower(): classificationWords[c] |= SCORE
		if "animated" in category.lower(): classificationWords[c] |= ANIMATED
		if "foreign" in category.lower(): classificationWords[c] |= FOREIGN

categories = []

presenters2013 = ["Aziz Ansari", "Jason Bateman", "Kristen Bell", "John Krasinski", "Halle Berry",
				   "Jessica Alba", "Kiefer Sutherland", "Don Cheadle", "Eva Longoria", "George Clooney",
				   "Sacha Baron Cohen", "Bradley Cooper", "Kate Hudson", "Robert Downey, Jr.", "Jimmy Fallon",
				   "Jay Leno", "Will Ferrell", "Kristen Wiig", "Nathan Fillion", "Lea Michele",
				   "Megan Fox", "Jonah Hill", "Jennifer Garner", "Salma Hayek", "Paul Rudd",
				   "Dustin Hoffman", "Lucy Liu", "Debra Messing", "Jennifer Lopez", "Jason Statham",
				   "Robert Pattinson", "Amanda Seyfried", "Dennis Quaid", "Kerry Washington", "Julia Roberts",
				   "Arnold Schwarzenegger", "Sylvester Stallone"]

presenters2015 = ["Amy Adams", "Jennifer Aniston", "Kate Beckinsale", "Adrien Brody",
				  "Bryan Cranston", "Benedict Cumberbatch", "Jamie Dornan", "Robert Downey, Jr.", "David Duchovny",
				  "Anna Faris", "Colin Farrell", "Jane Fonda", "Harrison Ford",
				  "Ricky Gervais", "Bill Hader", "Kevin Hart", "Salma Hayek", "Katherine Heigl",
				  "Katie Holmes", "Dakota Johnson", "Jared Leto", "Adam Levine",
				  "Jennifer Lopez", "Matthew McConaughey", "Seth Meyers", "Sienna Miller",
				  "Lupita Nyong'o", "Gwyneth Paltrow", "Chris Pratt", "Jeremy Renner",
				  "Paul Rudd", "Meryl Streep", "Lily Tomlin", "Vince Vaughn",
				  "Kristen Wiig"]

results = []

def cleanParameters():
	print "Removing accented characters from presenter parameters."
	for p, presenter in enumerate(presenters):
		presenters[p] = Winners.stripAccents(presenters[p])

def extractTweets2013():
	return Winners.extractTweets2013()

def extractTweets2015():
	return Winners.extractTweets2015()

def extractRelevantTweets(year):
	n = 0
	print "Removing tweets that don't contain relevant words."
	relevantTweets = []
	for i, line in enumerate(open('tweets' + str(year) + '.txt', 'r')):
		present = re.compile(r'(?i)present')  # present[ed/ing/s]
		give = re.compile(r'(?i)(?:^| )g[ai]ve(?:[ \.,:;!]|$)')  # give/gave
		introduce = re.compile(r'(?i)introduc') # introduce

		# If the tweet contains any of the previous relevant words, then save; otherwise discard
		if any([present.search(line), give.search(line), introduce.search(line)]):
			n += 1
			relevantTweets.append(line)

	return relevantTweets

def pruneIrrelevantTweets(relevantTweets):
	prunedTweets = []
	prunedTweets = relevantTweets
	separator = '' if prunedTweets[0][-1] == '\n' else '\n'
	with open('prunedPresenterTweets.txt', 'w') as out_file:
		out_file.write(separator.join(prunedTweets))

def removeStopListWords():
	finalTweets = []

	# Generate array with stoplist words
	stoplist = []
	for i, word in enumerate(open("stoplist.txt", 'r')):
		stoplist.append(word.lower().rstrip())

	print "Removing all characters that are not alphanumeric, quotation marks, or \\n."
	print "Substituting accented letters."
	print "Removing words that are specified in stoplist.txt."
	for i, line in enumerate(open("prunedPresenterTweets.txt", 'r')):
		# First, remove everything that is not alphanumeric, ', or \n
		pattern = re.compile(r'[^ \'0-9a-zA-Z\n]+')
		line = pattern.sub('', line)

		# Then, substitute accented letters with non-accent equivalences
		line = unicodedata.normalize('NFD', unicode(line)).encode('ascii', 'ignore')

		# Finally, remove all stoplist words given in stoplist.txt
		difference = set(line.lower().split()) - set(stoplist)
		line = ' '.join(list(difference))

		finalTweets.append(line)

	# Saves final results to file
	with open('finalPresenterTweets.txt', 'w') as out_file:
		out_file.write('\n'.join(finalTweets))

def generateWinners():
	print "Generating points matrix to determine winner."
	# First, create zeroed out matrix
	points = Winners.zeros(len(categories), len(presenters))
	for i, line in enumerate(open("finalPresenterTweets.txt", 'r')):
		for c, category in enumerate(categories):
			# Check if there are any matching words between tweet and category
			categoryWords = list(set(categories[c].lower().split()) & set(line.lower().split()))
			# If there were no matching words, continue (i.e. there MUST be at least one matching word to modify the matrix)
			if len(categoryWords) == 0:
				continue
			if (((not (classificationWords[c] & MOTION_PICTURE)) and ("motion" in line)) or
			    ((not (classificationWords[c] & TELEVISION)) and ("television" in line)) or
			    ((not (classificationWords[c] & DRAMA)) and ("drama" in line)) or
			    ((not (classificationWords[c] & COMEDY)) and ("comedy" in line)) or
			    ((not (classificationWords[c] & ACTOR)) and ("actor" in line)) or
			    ((not (classificationWords[c] & ACTRESS)) and ("actress" in line)) or
			    ((not (classificationWords[c] & SUPPORTING)) and ("supporting" in line)) or
			    ((not (classificationWords[c] & SONG)) and ("song" in line)) or
			    ((not (classificationWords[c] & SCORE)) and ("score" in line)) or
			    ((not (classificationWords[c] & ANIMATED)) and ("animated" in line)) or
			    ((not (classificationWords[c] & FOREIGN)) and ("foreign" in line)) or
			    (((classificationWords[c] & ACTOR)) and not ("actor" in line)) or
			    (((classificationWords[c] & ACTRESS)) and not ("actress" in line)) or
			    (((classificationWords[c] & DRAMA)) and not ("drama" in line))):
				continue
			# For each presenter
			for p, presenter in enumerate(presenters):
				# Check if there are any matching words between tweet and presenter
				presenterWords = list(set(presenters[p].lower().split()) & set(line.lower().split()))
				# If there were matching words, add value to matrix (i.e. there MUST be at least one matching word for both category and presenter)
				if len(presenterWords) > 0:
					points[c][p] += len(categoryWords) + len(presenterWords)
	#print points
	# Weights matrix by dividing all values by the amount of times that presenter was mentioned in all categories
	#weightSum = [sum([row[i] for row in points]) for i in range(0, len(points[0]))] # Adds columns and stores as list
	#for c, category in enumerate(points):
	#	for p, presenter in enumerate(category):
	#		points[c][p] = float(points[c][p])/float(weightSum[p])


	return points

def displayWinners(points, jsonDict):
	text = ""

	points = transpose(points)
	for p, presenter in enumerate(points):
		print "Presenter: " + presenters[p]
		print "\t" + categories[presenter.index(max(presenter))]
		
		if (jsonDict):
			jsonDict["data"]["structured"][categories[presenter.index(max(presenter))]]["presenters"].append(presenters[p].lower())
			jsonDict["data"]["unstructured"]["presenters"].append(presenters[p].lower())

	#for c, category in enumerate(points):
	#	print "Category: " + categories[c]
	#	print "\t" + presenters[category.index(max(category))]
	#	text += "Category: " + categories[c] + "\n"
	#	text += "\t" + presenters[category.index(max(category))] + "\n"
	return text

def findPresenters(year, jsonDict):
	global categories
	global presenters
	categories = Winners.categories2013 if year == 2013 else Winners.categories2015
	presenters = presenters2013 if year == 2013 else presenters2015

	cleanParameters()
	buildClassifications()
	extractTweets2013() if year == 2013 else extractTweets2015()
	relevantTweets = extractRelevantTweets(year)
	pruneIrrelevantTweets(relevantTweets)
	removeStopListWords()
	points = generateWinners()
	text = displayWinners(points, jsonDict)

	print "Done"