def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    for lst in data:
        if actor_id_1 in lst and actor_id_2 in lst:
            return True
        
    return False



def get_actors_with_bacon_number(data, n):
	"""Find all actors that have a bacon number of n
	"""
	BACON_NUM_ACTORS = {x : set() for x in xrange(n+1)}
	BACON_NUM_ACTORS[0] = set([4724])

	filmdict = create_filmdict(data)
	for i in xrange(n+1):
		BACON_NUM_ACTORS[i+1] = get_next_bacon_actors(BACON_NUM_ACTORS, i, filmdict)

	return sorted(list(BACON_NUM_ACTORS[n]))



def create_filmdict(data):
	"""Create a dictionary where key is film id and value is set of actors in that film id
	"""

	filmdict = {}
	
	for actor_pair in data:
		try: # add actors to the cast of a film
			filmdict[actor_pair[2]].add(actor_pair[0])
			filmdict[actor_pair[2]].add(actor_pair[1])
		except KeyError: # if film doesn't exist in filmdict create key and add the two actors
			filmdict[actor_pair[2]] = set([actor_pair[0],actor_pair[1]])
			
	return filmdict

def create_actordict(data):
	"""Create dictionary where key is actor id and value is set of films the actor has been in
	"""
	actordict = {}

	for lst in data:
		try: # add films to an actor's filmography
			actordict[lst[0]].add(lst[2])
			actordict[lst[1]].add(lst[2])
		except KeyError: # if actor doesn't exist in actordict create actor entry and add film
			actordict[lst[0]] = set([lst[2]])
			actordict[lst[1]] = set([lst[2]])
	return actordict


    

def get_next_bacon_actors(bacon_actors, i, actor_dict):
	"""take all actors with a Bacon number of i and returns all actors with a Bacon number of i+1"""    

	next_bacon_level = set()

	for film_id in actor_dict:
		for bacon_connected_actor in bacon_actors[i]:
			if bacon_connected_actor in actor_dict[film_id]:
				for new_connected_actor in actor_dict[film_id]:
					if new_connected_actor != bacon_connected_actor and not has_lower_number(bacon_actors, i+1, new_connected_actor):
						next_bacon_level.add(new_connected_actor) 

	return next_bacon_level


def has_lower_number(bacon_actors, current_bacon_num, actor):
	"""checks to see if actor has lower bacon number"""

	for i in xrange(current_bacon_num):
		if actor in bacon_actors[i]:
			return True
	return False



def get_bacon_path(data, actor_id):
	"""Find a path of actors that connects Kevin Bacon(actor_id = 4724) to actor_id
	"""
	actordict = create_actordict(data)
	filmdict = create_filmdict(data)
	actorgraph = create_actor_graph(actordict, filmdict)


	possible_paths = []

	possible_paths.append([4724]) # add Kevin Bacon
	checked  = set()

	while possible_paths:

		path = possible_paths.pop(0)

		node = path[-1]

		if node == actor_id:
			return path

		for adjacent in actorgraph.get(node, []):
			new_path = list(path)
			
			if adjacent not in checked:
				checked.add(adjacent)
				new_path.append(adjacent)
				possible_paths.append(new_path)
	
	return 



def create_actor_graph(actordict, filmdict):
	"""Create dictionary where key is actor and value is the set of actors that the key actor has performed with
	"""
	actorgraph = {k : set() for k in actordict}
	for actor in actordict:
		for films in actordict[actor]:
			actorgraph[actor] |= filmdict[films].difference([actor])
	return actorgraph






    
