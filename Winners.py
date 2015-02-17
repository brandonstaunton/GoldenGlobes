# -*- coding: iso-8859-15 -*-
from Tkinter import *
import json
import unicodedata
import pprint
import os.path

# URL: http://www.imdb.com/awards-central/golden-globes
# Javascript:
# for(var i = 0; i < 25; i++)
# {
# anchors = document.getElementsByClassName("nominees")[i].getElementsByTagName("a");
#   console.log('"' + anchors[0].innerHTML + '", "' + anchors[1].innerHTML + '", "' + anchors[2].innerHTML + '", "' + anchors[3].innerHTML + '"');
# }


# URL: http://www.imdb.com/awards-central/golden-globes
# Javascript: 
# for(var i = 0; i < 25; i++)
# {
#   anchors = document.getElementsByClassName("nominees")[i].getElementsByTagName("strong");
#   str = '"' + anchors[0].getElementsByTagName("a")[0].innerHTML + '"';
#   for(var j = 1; j < 4; j++)
#      str += ', "' + anchors[j].getElementsByTagName("a")[0].innerHTML + '"'
#   console.log(str)
# }

categories = []
nominees = []

categories2015 = ["Best Motion Picture Drama",
			  "Best Motion Picture - Musical or Comedy",
			  "Best Performance by an Actor in a Motion Picture - Drama",
			  "Best Performance by an Actress in a Motion Picture - Drama",
			  "Best Performance by an Actor in a Motion Picture - Musical or Comedy",
			  "Best Performance by an Actress in a Motion Picture - Musical or Comedy",
			  "Best Performance by an Actor in a Supporting Role in a Motion Picture",
			  "Best Performance by an Actress in a Supporting Role in a Motion Picture",
			  "Best Director - Motion Picture",
			  "Best Screenplay - Motion Picture",
			  "Best Original Song - Motion Picture",
			  "Best Original Score - Motion Picture",
			  "Best Animated Feature Film",
			  "Best Foreign Language Film",
			  "Best Television Series - Drama",
			  "Best Television Series - Musical or Comedy",
			  "Best Mini-Series or Motion Picture Made for Television",
			  "Best Performance by an Actor in a Television Series - Drama",
			  "Best Performance by an Actress in a Television Series - Drama",
			  "Best Performance by an Actor in a Television Series - Musical or Comedy",
			  "Best Performance by an Actress in a Television Series - Musical or Comedy",
			  "Best Performance by an Actor in a Mini-Series or a Motion Picture Made for Television",
			  "Best Performance by an Actress in a Mini-Series or a Motion Picture Made for Television",
			  "Best Performance by an Actor in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television",
			  "Best Performance by an Actress in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television"]

nominees2015 = [["Boyhood", "Selma", "The Imitation Game", "Foxcatcher", "The Theory of Everything"],
			["The Grand Budapest Hotel", "Birdman", "St. Vincent", "Into the Woods", "Pride"],
			["Eddie Redmayne", "Steve Carell", "Benedict Cumberbatch", "Jake Gyllenhaal", "David Oyelowo"],
			["Julianne Moore", "Jennifer Aniston", "Rosamund Pike", "Reese Witherspoon", "Felicity Jones"],
			["Michael Keaton", "Ralph Fiennes", "Christoph Waltz", "Bill Murray", "Joaquin Phoenix"],
			["Amy Adams", "Emily Blunt", "Julianne Moore", "Helen Mirren", "Quvenzhane Wallis"],
			["J.K. Simmons", "Robert Duvall", "Mark Ruffalo", "Ethan Hawke", "Edward Norton"],
			["Patricia Arquette", "Keira Knightley", "Emma Stone", "Meryl Streep", "Jessica Chastain"],
			["Richard Linklater", "Alejandro Gonzalez Inarritu", "Ava DuVernay", "David Fincher", "Wes Anderson"],
			["Birdman", "Boyhood", "Gone Girl", "The Imitation Game", "The Grand Budapest Hotel"],
			["Selma", "Lana Del Rey", "Patti Smith", "Sia", "Lorde"],
			["the imitation game", "birdman", "gone girl", "interstellar","the theory of everything"],
			["How to Train Your Dragon 2", "The Book of Life", "The Boxtrolls", "Big Hero 6", "The Lego Movie"],
			["Leviathan", "Ida", "Force Majeure", "Gett: The Trial of Viviane Amsalem", "Tangerines"],
			["The Affair", "Downton Abbey", "The Good Wife", "House of Cards", "Game of Thrones"],
			["Transparent", "Girls", "Orange Is the New Black", "Silicon Valley", "Jane the Virgin"],
			["Fargo", "Olive Kitteridge", "True Detective", "The Missing", "The Normal Heart"],
			["Kevin Spacey", "Liev Schreiber", "James Spader", "Dominic West", "Clive Owen"],
			["Ruth Wilson", "Robin Wright", "Julianna Margulies", "Viola Davis", "Claire Danes"],
			["Jeffrey Tambor", "Don Cheadle", "Ricky Gervais", "William H. Macy", "Louis C.K."],
			["Gina Rodriguez", "Lena Dunham", "Edie Falco", "Julia Louis-Dreyfus", "Taylor Schilling"],
			["Billy Bob Thornton", "Martin Freeman", "Matthew McConaughey", "Woody Harrelson", "Mark Ruffalo"],
			["Maggie Gyllenhaal", "Jessica Lange", "Frances McDormand", "Frances O'Connor", "Allison Tolman"],
			["Matt Bomer", "Jon Voight", "Alan Cumming", "Bill Murray", "Colin Hanks"],
			["Joanne Froggatt", "Allison Janney", "Uzo Aduba", "Kathy Bates", "Michelle Monaghan"]]


categories2013 = ["BEST MOTION PICTURE - DRAMA", 
			  "BEST PERFORMANCE BY AN ACTRESS IN A MOTION PICTURE - DRAMA", 
			  "BEST PERFORMANCE BY AN ACTOR IN A MOTION PICTURE - DRAMA", 
			  "BEST MOTION PICTURE - COMEDY OR MUSICAL", 
			  "BEST PERFORMANCE BY AN ACTRESS IN A MOTION PICTURE - COMEDY OR MUSICAL", 
			  "BEST PERFORMANCE BY AN ACTOR IN A MOTION PICTURE - COMEDY OR MUSICAL", 
			  "BEST ANIMATED FEATURE FILM", 
			  "BEST FOREIGN LANGUAGE FILM", 
			  "BEST PERFORMANCE BY AN ACTRESS IN A SUPPORTING ROLE IN A MOTION PICTURE", 
			  "BEST PERFORMANCE BY AN ACTOR IN A SUPPORTING ROLE IN A MOTION PICTURE", 
			  "BEST DIRECTOR - MOTION PICTURE", 
			  "BEST SCREENPLAY - MOTION PICTURE", 
			  "BEST ORIGINAL SCORE - MOTION PICTURE", 
			  "BEST ORIGINAL SONG - MOTION PICTURE", 
			  "BEST TELEVISION SERIES - DRAMA", 
			  "BEST PERFORMANCE BY AN ACTRESS IN A TELEVISION SERIES - DRAMA", 
			  "BEST PERFORMANCE BY AN ACTOR IN A TELEVISION SERIES - DRAMA", 
			  "BEST TELEVISION SERIES - COMEDY OR MUSICAL", 
			  "BEST PERFORMANCE BY AN ACTRESS IN A TELEVISION SERIES - COMEDY OR MUSICAL", 
			  "BEST PERFORMANCE BY AN ACTOR IN A TELEVISION SERIES - COMEDY OR MUSICAL", 
			  "BEST MINI-SERIES OR MOTION PICTURE MADE FOR TELEVISION", 
			  "BEST PERFORMANCE BY AN ACTRESS IN A MINI-SERIES OR MOTION PICTURE MADE FOR TELEVISION", 
			  "BEST PERFORMANCE BY AN ACTOR IN A MINI-SERIES OR MOTION PICTURE MADE FOR TELEVISION", 
			  "BEST PERFORMANCE BY AN ACTRESS IN A SUPPORTING ROLE IN A SERIES, MINI-SERIES OR MOTION PICTURE MADE FOR TELEVISION", 
			  "BEST PERFORMANCE BY AN ACTOR IN A SUPPORTING ROLE IN A SERIES, MINI-SERIES OR MOTION PICTURE MADE FOR TELEVISION"]

		  			  


nominees2013 = [["Django Unchained","Life of Pi","Lincoln","Zero Dark Thirty", "Argo"],
			["Marion Cotillard", "Helen Mirren","Naomi Watts", "Rachel Weisz", "Jessica Chastain"],
			["Richard Gere", "John Hawkes", "Joaquin Phoenix", "Denzel Washington", "Daniel Day Lewis"],
			["The Best Exotic Marigold Hotel", "Moonrise Kingdom", "Salmon Fishing in the Yemen", "Silver Linings PLaybook", "Les Miserables"],
			["Emily Blunt","Judi Dench","Maggie Smith","Meryl Streep","Jennifer Lawrence"],
			["Jack Black","Bradley Cooper","Ewan McGregor","Bill Murray","Hugh Jackman"],
			["Frankenweenie","Hotel Transylvania","Rise of the Guardians","Wreck-it Ralph","Brave"],
			["A Royal Affair","The Intouchables","Kon-tiki","Rust and Bone","Amour"],
			["Amy Adams","Sally Field","Helen Hunt","Nicole Kidman","Anne Hathaway"],
			["Alan Arkin","Leonardo DiCaprio","Philip Seymour Hoffman","Tommy Lee Jones","Christoph Waltz"],
			["Kathryn Bigelow","Ang Lee","Steven Spielberg","Quentin Tarantino","Ben Affleck"],
			["zero dark thirty", "lincoln", "silver linings playbook", "argo","Django Unchained"],
			["life pf pi","argo", "anna karenina", "cloud atlas", "lincoln"],
			["act of valor", "stand up guys", "the hunger games", "les miserables","skyfall"],
			["Breaking Bad","Boardwalk Empire","Downton Abbey: Season 2","The Newsroom","Homeland"],
			["Connie Britton","Glenn Close","Michelle Dockery","Julianna Margulies","Claire Danes"],
			["Steve Buscemi","Bryan Cranston","Jeff Daniels","Jon Hamm","Damian Lewis"],
			["The Big Bang Theory","Episodes","Modern Family","Smash","Girls"],
			["Zooey Deshanel","Julia Louis-Dreyfus","Tina Fey","Amy Peohler","Lena Dunham"],
			["Alec Baldwin","Louis C.K.","Matt LeBlanc","Jim Parsons","Don Cheadle"],
			["The Girl","Hatfields & McCoys","The Hour","Political Animals","Game Change"],
			["Nicole Kidman", "jessica Lange","Sienna Miller","Sigourney Weaver","Julianne Moore"],
			["Benedict Cumberbatch","Woody Harrelson","Toby Jones","Clive Owen","Kevin Costner"],
			["Hayden Panettiere","Archie Panjabi","Sarah Paulson","Sofia Vergara","Maggie Smith"],
			["Max Greenfield","Danny Huston","Mandy Patinkin","Eric Stonestreet","Ed Harris"]]
	

#for c, category in enumerate(nominees):
#	for e, element in enumerate(category):
#		nominees[c][e] = nominees[c][e].encode('utf-8')

def stripAccents(s):
	s = re.sub(r'[áàä]', r'a', s)
	s = re.sub(r'[éèë]', r'e', s)
	s = re.sub(r'[íìï]', r'i', s)
	s = re.sub(r'[óòö]', r'o', s)
	s = re.sub(r'[úùü]', r'u', s)
	s = re.sub(r'[ÁÀÄ]', r'A', s)
	s = re.sub(r'[ÉÈË]', r'E', s)
	s = re.sub(r'[ÍÌÏ]', r'I', s)
	s = re.sub(r'[ÓÒÖ]', r'O', s)
	s = re.sub(r'[ÚÙÜ]', r'U', s)
	return s

def cleanParameters():
	print "Removing accented characters from category and nominee parameters."
	for c, category in enumerate(categories):
		categories[c] = stripAccents(categories[c])
	for c, category in enumerate(nominees):
		for n, nominee in enumerate(category):
			nominees[c][n] = stripAccents(nominees[c][n])

def zeros(h, w):
# Creates an h by w matrix populated by 0s
	return [[0]*w for _ in xrange(h)]

def extractTweets2013():
# Extracts the full text of all the tweets from the full .json file provided (i.e. the 2015 file) and saves as "tweets.txt"
	if os.path.isfile("tweets2013.txt"):
		print "WARNING: tweets2013.txt already exists. Using this file instead of generating new one. Delete existing file if you want to generate a new one."
		return
	print "Extracting all tweets from .json file."
	tweets = []
	# Go through tweets and extract only tweet text
	for i, line in enumerate(open("gg2013.json", 'r')):
		# goldenglobes2015
		# gg2013
		alldata = json.loads(line)

		for data in alldata:

			# If tweet text is cut off at the end, check if full text exists in retweeted status
			if data['text'][-1] == u'\u2026' and 'retweeted_status' in data:
				text = data['retweeted_status']['text'].encode('utf-8')
			# If it is not cut off or if no alternate full text exists, use original tweet text
			else:
				text = data['text'].encode('utf-8')
			# Finally, remove all line breaks within individual tweets
			text = text.replace("\n", " ")
			#if i % 100000 == 0:
			#	print "\t" + str(i) + " tweets processed"

			tweets.append(text+'\n')

	# Save all tweets to file
	separator = '' if tweets[0][-1] == '\n' else '\n'
	with open('tweets2013.txt', 'w') as out_file:
		out_file.write(separator.join(tweets))

def extractTweets2015():
# Extracts the full text of all the tweets from the full .json file provided (i.e. the 2015 file) and saves as "tweets.txt"
	if os.path.isfile("tweets2015.txt"):
		print "WARNING: tweets2015.txt already exists. Using this file instead of generating new one. Delete existing file if you want to generate a new one."
		return
	print "Extracting all tweets from .json file."
	tweets = []
	# Go through tweets and extract only tweet text
	for i, line in enumerate(open("goldenglobes2015.json", 'r')):
		# goldenglobes2015
		# gg2013
		data = json.loads(line)

		
		# If tweet text is cut off at the end, check if full text exists in retweeted status
		if data['text'][-1] == u'\u2026' and 'retweeted_status' in data:
			text = data['retweeted_status']['text'].encode('utf-8')
		# If it is not cut off or if no alternate full text exists, use original tweet text
		else:
			text = data['text'].encode('utf-8')
		# Finally, remove all line breaks within individual tweets
		text = text.replace("\n", " ")
		#if i % 100000 == 0:
		#	print "\t" + str(i) + " tweets processed"

		tweets.append(text)

		# Save all tweets to file
	separator = '' if tweets[0][-1] == '\n' else '\n'
	with open('tweets2015.txt', 'w') as out_file:
		out_file.write(separator.join(tweets))

def extractRelevantTweets(year):

# Saves only the tweets with the specified relevant words, and saves as "relevantTweets.txt"
	# Relevant words: {winner, winners, win, wins, won, goes to, went to, victory, receive, congrats, congratulations}
	print "Removing tweets that don't contain relevant words."
	relevantTweets = []
	for i, line in enumerate(open('tweets' + str(year) + '.txt', 'r')):
		win = re.compile(r'(?i)(?:^| )w[io]n(?:ner|ning)?s?(?:[ \.,:;!]|$)')  # win(s), won, winner(s), winning(s)
		go = re.compile(r'(?i)(?:^| )(?:went|go|goes)(?:[ \.,:;!]|$)')  # went, go, goes
		receive = re.compile(r'(?i)(?:^| )(?:receive[sd]?)(?:[ \.,:;!]|$)')  # receive(s), receive(d)
		victory = re.compile(r'(?i)(?:^| )victory(?:[ \.,:;!]|$)')  # victory
		congrats = re.compile(
			r'(?i)(?:^| )(?:congrat(?:s|ulat(?:ions|ed)))(?:[ \.,:;!]|$)')  # congrats, congratulated, congratulations

		# If the tweet contains any of the previous relevant words, then save; otherwise discard
		if any([win.search(line), go.search(line), receive.search(line), victory.search(line), congrats.search(line)]):
			relevantTweets.append(line)

	return relevantTweets

def pruneIrrelevantTweets(relevantTweets):
# Remove tweets that contain the irrelevant words listed below, and save in "prunedTweets.txt"
	# Irrelevant words: {never, didn't, I hope, luck}
	# Disappoint(ed/ing), bummed, etc. are unnecessary, since didn't is an irrelevant word
	print "Removing tweets that contain irrelevant words."
	prunedTweets = []
	for i, line in enumerate(relevantTweets):
		never = re.compile(r'(?i)(?:^| )never(?:[ \.,:;!]|$)')  # never
		didnt = re.compile(r'(?i)(?:^| )did(?:n\'t| not)(?:[ \.,:;!]|$)')  # didn't, did not
		hope = re.compile(r'(?i)(?:^| )i hope(?:[ \.,:;!]|$)')  # I hope
		luck = re.compile(r'(?i)(?:^| )luck(?:[ \.,:;!]|$)')  # luck
		prediction = re.compile(r'(?i)(?:^| )predictions?(?:[ \.,:;!]|$)')

		# If tweet does not contain any of the specified irrelevant words, then save; otherwise discard
		if (not any([never.search(line), didnt.search(line), hope.search(line), luck.search(line), prediction.search(line)])):
			prunedTweets.append(line)

	# Save specified tweets to file
	separator = '' if prunedTweets[0][-1] == '\n' else '\n'
	with open('prunedWinnerTweets.txt', 'w') as out_file:
		out_file.write(separator.join(prunedTweets))

def removeStopListWords():
# This does not delete any tweets. It simply removes the stop list words saved in "stoplist.txt"
# This reorganizes the individual tweets' word order, so they are not longer syntactically correct (in English)
# This method also does other minor changes, like remove all non-alphanumeric symbols and substitute accented words
# Results are saved in "finalTweets.txt"
	finalTweets = []

	# Generate array with stoplist words
	stoplist = []
	for i, word in enumerate(open("stoplist.txt", 'r')):
		stoplist.append(word.lower().rstrip())

	print "Removing all characters that are not alphanumeric, quotation marks, or \\n."
	print "Substituting accented letters."
	print "Removing words that are specified in stoplist.txt."
	for i, line in enumerate(open("prunedWinnerTweets.txt", 'r')):
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
	with open('finalWinnerTweets.txt', 'w') as out_file:
		out_file.write('\n'.join(finalTweets))

def generateWinners():
# Generates a numerical matrix that represents each category and nominees for each category
#   In this specfic case, there are 25 categories and 5 nominees per category, so the matrix would be 25 by 5
# For each tweet, checks if it contains the words in each category and nominee.
#   If it contains words in BOTH the category and nominee, then it adds the amount of words that matched
	print "Generating points matrix to determine winner (takes approx 1 minute)."
	# First, create zeroed out matrix
	points = zeros(len(categories), len(nominees[0]))

	# For each tweet
	for i, line in enumerate(open("finalWinnerTweets.txt", 'r')):
	
		
		# For each category
		for c, category in enumerate(categories):
			# Check if there are any matching words between tweet and category
			categoryWords = list(set(categories[c].lower().split()) & set(line.lower().split()))
			# If there were no matching words, continue (i.e. there MUST be at least one matching word to modify the matrix)
			if len(categoryWords) == 0:
				continue

			if (("actor" in categories[c].lower()) != ("actor" in line.lower())):
				continue

			if (("actress" in categories[c].lower()) != ("actress" in line.lower())):
				continue
			
			# For each nominee
			for n, nominee in enumerate(nominees[c]):
				# Check if there are any matching words between tweet and nominee
				nomineeWords = list(set(nominees[c][n].lower().split()) & set(line.lower().split()))
				# If there were matching words, add value to matrix (i.e. there MUST be at least one matching word for both category and nominee)
				if len(nomineeWords) >= max(int(len(nominees[c][n].split())/2),1):
					if nominees[c][n].lower().split()[-1] in line.lower():
						points[c][n] += len(categoryWords) #+ len(nomineeWords)
	#print points				
	return points

def displayWinners(points, jsonDict, year):
# Coherently displays who the winners are for each category, as well as the respective nominees
	
	#load meta data here
	if (jsonDict == {}):
		metadata = {}
		metadata["year"] = year
		methodList = ["hosts","nominees","awards"]
		method=      ["hardcoded","hardcoded","hardcoded"]
		methodDescription = ["","",""]
		for index,word in enumerate(methodList):
			metadata[word] = {}
			metadata[word]["method"] = method[index]
			metadata[word]["method_description"] = methodDescription[index]
		jsonDict["metadata"] = metadata

		#load data field data here
		data = {}
		#building unstructured data here
		data["unstructured"] = {}
		data["unstructured"]["awards"] = categories;
		data["unstructured"]["nominees"] = []
		data["unstructured"]["winners"] = []
		#little hard code here....
		for array in nominees:
			for name in array:
				data["unstructured"]["nominees"].append(name.lower())
		data["unstructured"]["hosts"] = []
		data["unstructured"]["presenters"] = []
		#buliding structrue data here
		data["structured"] = {}
		for c,category in  enumerate(points):
			data["structured"][categories[c]] = {}
			data["structured"][categories[c]]["winner"] = nominees[c][points[c].index(max(points[c]))].lower()
			data["unstructured"]["winners"].append(nominees[c][points[c].index(max(points[c]))].lower())
			#print data["structured"][categories[c]]["winner"]
			data["structured"][categories[c]]["presenters"] = []
			data["structured"][categories[c]]["nominees"] = []
			for n in range(len(nominees[c])):
				if n!= points[c].index(max(points[c])):
					data["structured"][categories[c]]["nominees"].append(nominees[c][n].lower())


		#print data["structured"][categories[c]]["nominees"]
	#finish building 
		jsonDict["data"] = data
	#finish building json

	
# Coherently displays who the winners are for each category, as well as the respective nominees
	for c, category in enumerate(points):
		print categories[c] + ":"
		print "\tWinner: " + nominees[c][points[c].index(max(points[c]))] #+ " (" + str(points[c].index(max(points[c]))) + ")"
		print "\tNominees: " + ', '.join([nominees[c][n] for n in range(len(nominees[c])) if n != points[c].index(max(points[c]))])
	
	return;

def findAwards(year, jsonDict):
	global categories
	global nominees
	categories = categories2013 if year == 2013 else categories2015
	nominees = nominees2013 if year == 2013 else nominees2015

	cleanParameters()
	extractTweets2013() if year == 2013 else extractTweets2015()
	relevantTweets = extractRelevantTweets(year)
	pruneIrrelevantTweets(relevantTweets)
	removeStopListWords()
	points = generateWinners()
	text = displayWinners(points, jsonDict, year)