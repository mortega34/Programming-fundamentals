def find_shortest_path(graph, start, end, twisty):
    # Remember to return a list of edges as defined in README
    # i.e.: [{"start":[x1,y1], "end":[x2,y2]}, {"start":[x2,y2], "end":[x3,y3]}]

    graph = create_new_graph(graph)

    possible_paths = []
    #checked = set()
    visited = {}

    #add starting point
    possible_paths.append([start])


    while possible_paths:

    	path = possible_paths.pop(0)

    	node = path[-1]

    	if node == end:
    		return format_answer(path)


    	for adjacent in graph.get(tuple(node),[]):
    		new_path = list(path)

    		if len(path) == 1:
                # handle the starting point
    			visited[tuple(adjacent)] = [[adjacent[0]-node[0], adjacent[1]-node[1]]]
    			new_path.append(adjacent)
    			possible_paths.append(new_path)
    		elif isEligible(node, adjacent, path[-2], twisty):
    			vector_one = [node[0]-path[-2][0], node[1]-path[-2][1]]
    			if tuple(adjacent) not in visited:
    				visited[tuple(adjacent)] = [vector_one]
    				new_path.append(adjacent)
    				possible_paths.append(new_path)
    			elif tuple(adjacent) in visited and vector_one not in visited[tuple(adjacent)]:
    				visited[tuple(adjacent)].append(vector_one)
    				new_path.append(adjacent)
    				possible_paths.append(new_path)




    return


def format_answer(path):
	result = []
	path_length = len(path)
	for i, current_point in enumerate(path):
		if i < path_length-1:
			result.append({'start': current_point, 'end': path[i+1]})

	return result

def create_new_graph(edges):
	"""Create new graph where key is a point and value is all adjacent points
	"""
	result = {}

	for edge in edges:
		result.setdefault(tuple(edge['start']), []).append(edge['end'])


	return result



def isEligible(current, next, former, twisty):
	vector_one = [former[0]-current[0], former[1]-current[1]]
	vector_two = [current[0]-next[0], current[1]-next[1]]
	if turn_direction(vector_one,vector_two) == "u-turn":
		return False
	if twisty:
		if turn_direction(vector_one,vector_two) == "straight":
			return False
	else:
		if turn_direction(vector_one,vector_two) == "left":
			return False
	return True

def turn_direction(d1, d2):
	cross_p = cross_product(d1,d2)
	if cross_p == 0:
		if dot_product(d1,d2) < 0: #U-turn condition which is NEVER allowed
			return "u-turn"
		else:
			return "straight"
	elif cross_p < 0:
		return "left"
	return "right"

def cross_product(d1, d2):
	return d1[0]*d2[1] - d1[1]*d2[0]

def dot_product(d1, d2):
	return d1[0]*d2[0] + d1[1]*d2[1]

## BONUS
def find_shortest_path_bonus(graph, start, end, num_left_turns):
    # Remember to return a list of edges as defined in README
    # i.e.: [{"start":[x1,y1], "end":[x2,y2]}, {"start":[x2,y2], "end":[x3,y3]}]
    return []



#print find_shortest_path([{"start":[1,1], "end":[1,0]},{"start":[1,2], "end":[1,1]},{"start":[3,0], "end":[2,0]},{"start":[1,4], "end":[2,3]},{"start":[2,3], "end":[3,3]},{"start":[2,3], "end":[2,2]},{"start":[2,2], "end":[3,2]},{"start":[3,2], "end":[3,1]},{"start":[3,2], "end":[4,2]},{"start":[3,3], "end":[4,3]},{"start":[3,1], "end":[4,1]},{"start":[4,2], "end":[4,1]},{"start":[4,3], "end":[4,2]}], [1,4], [4,1], True)
