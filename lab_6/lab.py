from string import ascii_lowercase

def generate_trie(words):
	"""
	take as input words, a list of words representing a corpus, and return a trie representing that list of words. 
	words is  guaranteed to contain words consisting only of lowercase letters.
	"""
	root  = {'frequency': 0, 'children': {}}
	frequencies = {}
	
	for word in words:
		current_dict = root['children']
		freq_word = ''
		for letter in word:
			freq_word += letter
			
			if freq_word in frequencies:
				next_level = {'frequency': frequencies[freq_word], 'children':{}}
			else:
				frequencies[freq_word] = words.count(freq_word)
				next_level = {'frequency': frequencies[freq_word], 'children':{}}

			current_dict = current_dict.setdefault(letter, next_level)
			current_dict = current_dict['children']
		
	return root

def autocomplete(trie, prefix, N):
	""" 
	return a list of the most-frequently-occurring N words in trie that start with prefix
	"""

	child_tree = get_child(trie['children'], prefix)
	suffix_list = suffixes(child_tree)	

	if isvalidWord(trie['children'], prefix):
		suffix_list.append([get_frequency(trie['children'],prefix), ''])

	suffix_list.sort()
	suffix_list.reverse()
	

	if len(suffix_list) <= N:
		return [prefix+i[1] for i in suffix_list]

	else:
		return [prefix+suffix_list[i][1] for i in xrange(N)]



def get_frequency(trie, prefix):
	if len(prefix) == 1:
		return trie[prefix]['frequency']

	return get_frequency(trie[prefix[0]]['children'], prefix[1:])

def isvalidWord(trie, prefix):
	try:
		if len(prefix) == 1 and trie[prefix]['frequency'] == 0:
			return False
		if len(prefix) == 1 and trie[prefix]['frequency'] > 0:
			return True

		return isvalidWord(trie[prefix[0]]['children'], prefix[1:])
	except KeyError:
		return False



def get_child(trie, prefix):
	try:
		if len(prefix) == 1:
			return trie[prefix[0]]['children']
		else:
			return get_child(trie[prefix[0]]['children'], prefix[1:])
	except KeyError:
		return {}


def suffixes(trie, suffix = ''):
	result = []


	for letter in trie:
		suffix += letter
		if trie[letter]['children']:
			if trie[letter]['frequency'] > 0:
				result.append([trie[letter]['frequency'], suffix])
			result.extend(suffixes(trie[letter]['children'], suffix))
		else:
			result.append([trie[letter]['frequency'], suffix])
			
		suffix = suffix[:-1]

	return result
		



def autocorrect(trie, prefix, N):
	""" 
	Should invoke autocomplete, but if fewer than N completions are made, suggest additional words 
	by applying one valid edit to the prefix.
	"""
	autocomplete_list = autocomplete(trie, prefix, N)
	result = []
	if len(autocomplete_list) >= N:
		return autocomplete_list
	result.extend(autocomplete_list)

	correction_list = []

	# generate a list of valid words using deletion edit
	deletion_list = deletion(trie, prefix)
	correction_list.extend(deletion_list) 

	# generate a list of valid words using insertion edit
	insertion_list = insertion(trie, prefix)
	correction_list.extend(insertion_list)

	# generate a list of valid words using replacement edit
	replacement_list = replacement(trie, prefix)
	correction_list.extend(replacement_list)

	# generate a list of valid words using transpose edit
	transpose_list = transpose(trie, prefix)
	correction_list.extend(transpose_list)

	# arrange possible corrections in order of frequency (high to low)
	correction_list.sort()
	correction_list.reverse()


	# check if C<N
	if (len(autocomplete_list) + len(correction_list)) < N:
		for i in correction_list:
			if i[1] not in result:
				result.append(i[1])
		return result

	# add N-C amount of correction to result list
	for i in xrange(N - len(autocomplete_list)):
		if correction_list[i][1] not in result:
			result.append(correction_list[i][1])

	return result

def deletion(trie, prefix):
	result = []
	
	for i in xrange(len(prefix)):
		deleted_word = prefix[:i]+prefix[i+1:]
		if isvalidWord(trie['children'], deleted_word):
			result.append([get_frequency(trie['children'], deleted_word), deleted_word])


	return result


def insertion(trie, prefix):
	result = []

	for letter in ascii_lowercase:
		for i in xrange(len(prefix)+1):
			inserted_word = prefix[:i] + letter + prefix[i:]
			if isvalidWord(trie['children'], inserted_word):
				result.append([get_frequency(trie['children'], inserted_word), inserted_word])

	return result


def replacement(trie, prefix):
	result = []

	for letter in ascii_lowercase:
		for i in xrange(len(prefix)):
			replaced_word = prefix[:i] + letter + prefix[i+1:]
			if isvalidWord(trie['children'], replaced_word):
				result.append([get_frequency(trie['children'], replaced_word), replaced_word])

	return result

def transpose(trie, prefix):
	result = []
	transposed_word = list(prefix[:])
	for i in xrange(len(prefix)-1):
		#swap letters
		transposed_word[i], transposed_word[i+1] = transposed_word[i+1], transposed_word[i]
		trans_string = "".join(transposed_word)

		if isvalidWord(trie['children'], trans_string):
			result.append([get_frequency(trie['children'], trans_string), trans_string])

		#swap back
		transposed_word[i], transposed_word[i+1] = transposed_word[i+1], transposed_word[i]

	return result


"""test = ["man","mat","mattress","map","me","met","a","man","a","a","a","map","man","met"]
test_trie = generate_trie(test)
prefix = 'm'

print suffixes(test_trie['children']), '\n'


print autocomplete(test_trie, prefix, 3)"""








