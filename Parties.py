import heapq
from pprint import pprint
import re
import unicodedata
import Winners

categories = []

def extractTweets2013():
	return Winners.extractTweets2013()

def extractTweets2015():
	return Winners.extractTweets2015()

def extractPartyRelevantTweets(year):
	print "Removing tweets that don't contain relevant words."
	relevantTweets = []
	for i, line in enumerate(open('tweets' + str(year) + '.txt', 'r')):
		party = re.compile(r'(?i)part(?:y|ies)(?:[ \.,:;!]|$)')  # party, parties, houseparty, house-party, etc
		house = re.compile(r'(?i)house') # the word house under any context

		# If the tweet contains any of the previous relevant words, then save; otherwise discard
		if any([party.search(line), house.search(line)]):
			relevantTweets.append(line)

	return relevantTweets

def removePartyStopListWords(relevantTweets):
	stopList = [e.lower() for e in list(set(' '.join(categories).split())) if e != "-"]
	stopList.append("golden globes")
	stopList.append("golden globe")
	stopList.append("after")
	stopList.append("party")
	prunedTweets = []

	for tweet in relevantTweets:
		remove = '|'.join(stopList)
		regex = re.compile(r'\b('+remove+r')\b', flags=re.IGNORECASE)
		prunedTweets.append(regex.sub("", tweet))

	separator = '' if prunedTweets[0][-1] == '\n' else '\n'
	with open('finalPartyTweets.txt', 'w') as out_file:
		out_file.write(separator.join(prunedTweets))

def generatePartyWinners():
	partyDictionary = {}
	for i, line in enumerate(open("finalPartyTweets.txt", 'r')):
		matches = re.findall(ur'([A-Z]{1,2}[a-z\']*[A-Z]?[a-z\']* (?:[A-Z]{1,2}[a-z\']*[A-Z]?[a-z\']* )?[A-Z]{1,2}[a-z\']*[A-Z]?[a-z\']*)(?:[ \.,:;!]|$)', line)
		for match in matches:
			if "best" in match.lower() or "series" in match.lower():
				continue
			if match in partyDictionary:
				partyDictionary[match] += 1
			else:
				partyDictionary[match] = 1
	pprint(partyDictionary)
	return partyDictionary

def displayPartyWinners(partyDictionary):
	mostRepeatedKeys = []

	values = list(partyDictionary.values())
	keys = list(partyDictionary.keys())

	nLargestElements = heapq.nlargest(10, values)
	for l in nLargestElements:
		index = values.index(l)
		mostRepeatedKeys.append(keys[index])
		del values[index]
		del keys[index]

	print "These are the most commonly mentioned events or attendees:"
	print '\t' + ', '.join(mostRepeatedKeys)

def parties(year):
	global categories
	categories = Winners.categories2013 if year == 2013 else Winners.categories2015

	extractTweets2013() if year == 2013 else extractTweets2015()
	relevantTweets = extractPartyRelevantTweets(year)
	removePartyStopListWords(relevantTweets)
	partyDictionary = generatePartyWinners()
	displayPartyWinners(partyDictionary)