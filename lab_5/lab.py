def pack(tentSize, missingSquares):
    # Take care to return a list of dictionaries with keys:
    #  "anchor": [x,y]
    #  "orientation": 0/1
    if (tentSize[0]*tentSize[1] - len(missingSquares)) % 3 !=0:
    	return False

    available_spaces = set()
    for i in xrange(tentSize[0]):
        for j in xrange(tentSize[1]):
            available_spaces.add((i,j))

    
    missingSquares = set([tuple(i) for i in missingSquares])

    available_spaces = available_spaces.difference(missingSquares)

    layout = []

    if available_spaces == set([]):
        return layout


    #place camper
    anchor = min(available_spaces)

    camper = {'anchor':anchor, 'orientation': 0}
    camper_1 = {'anchor':anchor, 'orientation': 1}

    if overlap_with_missing(camper,missingSquares) and overlap_with_missing(camper_1,missingSquares) and not onBoard(camper_1,tentSize) and not onBoard(camper,tentSize):
        return False


    #place horizontal camper
    if onBoard(camper,tentSize) and not overlap_with_missing(camper, missingSquares):
        missingSquares.add( tuple(camper['anchor']) )
        missingSquares.add( (camper['anchor'][0]+1, camper['anchor'][1]) )
        missingSquares.add( (camper['anchor'][0]+2, camper['anchor'][1]) )
        layout.append(camper)


        pack_hor = pack(tentSize, missingSquares)
        if  pack_hor == False:
            layout.remove(camper)
            missingSquares.remove( (camper['anchor'][0]+1, camper['anchor'][1]) )
            missingSquares.remove( (camper['anchor'][0]+2, camper['anchor'][1]) )
            missingSquares.remove(tuple(camper['anchor']))
        else:
            layout.extend(pack_hor)
            return layout

    

    #place vertical camper
    if onBoard(camper_1,tentSize) and not overlap_with_missing(camper_1, missingSquares):
        missingSquares.add( tuple(camper['anchor']) )
        missingSquares.add( (camper_1['anchor'][0], camper_1['anchor'][1]+1) )
        missingSquares.add( (camper_1['anchor'][0], camper_1['anchor'][1]+2) )
        layout.append(camper_1)

        pack_vert = pack(tentSize,missingSquares)
        if  pack_vert == False:
            layout.remove(camper_1)
            missingSquares.remove( (camper_1['anchor'][0], camper_1['anchor'][1]+1) )
            missingSquares.remove( (camper_1['anchor'][0], camper_1['anchor'][1]+2) )
            missingSquares.remove(tuple(camper['anchor']))
            
        else:
            layout.extend(pack_vert)
            return layout



    return False






def overlap_with_missing(camper, missingSquares):
	if camper['orientation'] == 0:
		for i in range(1,3):
			if ( (camper['anchor'][0]+i), camper['anchor'][1] ) in missingSquares:
				return True
	else:
		for i in range(1,3):
			if ( (camper['anchor'][0]), camper['anchor'][1]+i ) in missingSquares:
				return True
	return False




def onBoard(camper, tentSize):
	if camper['orientation'] == 0:
		if (camper['anchor'][0]+2) < tentSize[0]:
			return True
	else:
		if (camper['anchor'][1]+2) < tentSize[1]:
			return True
	return False

