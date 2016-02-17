#!/usr/bin/env python

import nltk, string, re


###############################
### Output data into a file ###

# Format: 'fname lname', 'key', 'value'
def output_items(fd):
	for k, v in fd:
		print repr(fname + " " + lname) + ", " + repr(k) + ", " + repr(v)


###########################
### Convert docx to txt ###
# unzip -p aa.docx | grep '<w:t' | sed 's/<[^<]*>//g' | grep -v '^[[:space:]]*$' > aa.txt

filename = 'aa.txt'
fname = 'Ian'
lname = 'Liew'


#################
### Read file ###
with open(filename, 'r') as f:
	text = f.read()


#####################
### Clean up text ###

### Remove non ascii characters
text = filter(lambda x: x in string.printable, text)

### Add space between words that are joint together
### E.g. HelloWorld -> Hello World
p = re.compile('(\w)([A-Z])')
text = p.sub('\\1 \\2', text)

### Add space between full stop and beginning of word
### E.g. Hello.World -> Hello. World
p = re.compile('(\w\.)(\w)')
text = p.sub('\\1 \\2', text)

### Remove name
p = re.compile('('+fname+')\s('+lname+')?')
text = p.sub('', text)


##############
### START ###

sentences = nltk.sent_tokenize(text)

tokens = nltk.word_tokenize(sentences[0])
	# you'd wanna be looping through all sentences in text
	# in this example, only use first the sentence
tokens = nltk.word_tokenize(text)
	# or rather, treat full text as a long sentence
tokens = [w for w in tokens if w not in string.punctuation]
tokens = [w for w in tokens if w not in nltk.corpus.stopwords.words("english")]


### Part 1: Most common word

fd = nltk.FreqDist(tokens)
#print "\n\n*** Most common word ***\n"
#print fd.most_common(20)
output_items(fd.most_common(20))


### Part 2: Named entities

tagged = nltk.pos_tag(tokens)
chunked = nltk.chunk.ne_chunk(tagged, binary=True)

def extract_entity_names(t):
	entity_names = []

	if hasattr(t, 'label') and t.label:
		if t.label() == 'NE':
			entity_names.append(' '.join([child[0] for child in t]))
		else:
			for child in t:
				entity_names.extend(extract_entity_names(child))

	return entity_names


entity_names = []
for tree in chunked:
	entity_names.extend(extract_entity_names(tree))

fd = nltk.FreqDist(entity_names)
#print "\n\n*** Most common named entities (using ne_chunk) ***\n"
#print fd.most_common(20)
output_items(fd.most_common(20))


### Part 3: ...


#print "\n\n\n"
