import Winners
import matplotlib.pyplot as plt
import numpy as np
import pprint
import re
import unicodedata

categories = []
nominees = []

def cleanParameters():
	Winners.cleanParameters()

def extractTweets2013():
	return Winners.extractTweets2013()

def extractTweets2015():
	return Winners.extractTweets2015()

def extractRelevantTweets(year):
# Saves only the tweets with the specified relevant words, and returns
	print "Removing tweets that don't contain relevant words."
	positiveRT = []
	negativeRT = [] 
	negative = re.compile(r'absurd|too bad|annoy|abuse|arrogant|awful|awkward|bias|boycott|condemn|contempt|crap|depress|despair|disaster|disgrace|hate|horrible|illegal|insane|insult|irony|mistake|mourn|painful|sad|shame')
	positive = re.compile(r'proud|happy|applaud|charming|admir(?:e|able)|adored?|amaz(?:ing|ed)|applaud|aspired|awesome|bless(?:ed)|bravo|charisma|cool|delighted|dignity|noble|excited|fond|hero|honored|incredible|joy|ovation|positive|prefer|satisf(?:y|ied)|powerful')
	for i, line in enumerate(open("tweets" + str(year) + ".txt", 'r')):
		if any ([positive.search(line)]):
			positiveRT.append("+"+line)
		elif any([negative.search(line)]):
			negativeRT.append("-"+line)
	final = positiveRT + negativeRT
	
	return final

def removeStopListWords(tweets):
# This does not delete any tweets. It simply removes the stop list words saved in "stoplist.txt"
# This reorganizes the individual tweets' word order, so they are not longer syntactically correct (in English)
# This method also does other minor changes, like remove all non-alphanumeric symbols and substitute accented words
# Results are saved in "finalTweets.txt"
	finalTweets = []

	# Generate array with stoplist words
	stoplist = []
	for i, word in enumerate(open("stoplist.txt", 'r')):
		stoplist.append(word.lower().rstrip())

	positive = True
	print "Removing all characters that are not alphanumeric, quotation marks, or \\n."
	print "Substituting accented letters."
	print "Removing words that are specified in stoplist.txt."
	for i, line in enumerate(tweets):
		# First, remove everything that is not alphanumeric, ', or \n
		if line[0]=='+':
			positive = True
		elif line[0]=='-':
			positive = False
		else:
			print "impossible: "+line
		pattern = re.compile(r'[^ \'0-9a-zA-Z\n]+')
		line = pattern.sub('', line)

		# Then, substitute accented letters with non-accent equivalences
		line = unicodedata.normalize('NFD', unicode(line)).encode('ascii', 'ignore')

		# Finally, remove all stoplist words given in stoplist.txt
		difference = set(line.lower().split()) - set(stoplist)
		line = ' '.join(list(difference))
		if positive:
			line = "+"+line
		else:
			line = "-"+line
		finalTweets.append(line)

	# Saves final results to file
	with open('finalSentimentTweets.txt', 'w') as out_file:
		out_file.write('\n'.join(finalTweets))

def getPoint():
	positivePoints = Winners.zeros(len(categories),len(nominees[0]))
	negativePoints = Winners.zeros(len(categories),len(nominees[0]))
	positive = True

	print "Generate scores for positive and negative sentiments"

	for i,line in enumerate(open("finalSentimentTweets.txt",'r')):
		if line[0]=='+':
			positive = True
		else:
			positive = False;
		line = line[1:] #this shall be both fine
		for c,category in enumerate(categories):
			for n,nominee in enumerate(nominees[c]):
				nomineeWords = list(set(line.lower().split())&set(nominees[c][n].lower().split()))
				if len(nomineeWords)>0:
					if positive:
						positivePoints[c][n] += len(nomineeWords)
					else:
						negativePoints[c][n] += len(nomineeWords)

	#pprint.pprint(positivePoints)
	print "#########################"
	#pprint.pprint(negativePoints)
	return positivePoints,negativePoints

def displaySentiments(points):
	#create new list
	#pair the scores with the list of nonimees respectively
	result = []
	for c,category in enumerate(points):
		result.append(zip(nominees[c],points[c]))

	return result;

def  generatePicture(data):
	#generate graph for the specified category
	N = (len(data))
	x = np.arange(1, N+1)
	y = [num for (s, num) in data]
	labels = [s for (s,num) in data]
	width = 1.2
	plt.bar(x, y, width, color='r', alpha=0.7)
	plt.ylabel('Sentiment Scores', fontsize='16')
	plt.xlabel("Nominees", fontsize='16')
	plt.xticks(x, labels, fontsize='6', rotation=90)
	
	plt.show()
	return;

def sentimentAnalysis(year):
	global categories
	global nominees
	categories = Winners.categories2013 if year == 2013 else Winners.categories2015
	nominees = Winners.nominees2013 if year == 2013 else Winners.nominees2015

	cleanParameters()
	extractTweets2013() if year == 2013 else extractTweets2015()
	relevantTweets = extractRelevantTweets(year)
	removeStopListWords(relevantTweets)
	positive, negative = getPoint()
	Fpositive = displaySentiments(positive)
	Fnegative = displaySentiments(negative)
	
	AllPResult = []
	AllNResult = []

	for item in Fpositive:
		AllPResult = AllPResult+item

	for item in Fnegative:
		AllNResult = AllNResult+item

	generatePicture(AllPResult)
	generatePicture(AllNResult)